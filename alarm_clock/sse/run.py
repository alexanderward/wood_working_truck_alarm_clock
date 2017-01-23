import uuid
import signal

from Queue import Queue

import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
import sys

sys.path.append('..')
from pubsub.broker import Broker
from alarm_clock.settings import SSE_PORT
from tornado.options import define, options, parse_command_line
import threading

define("port", default=SSE_PORT, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()

is_closing = False


def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True


def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')


class PubSub(threading.Thread):
    def __init__(self, channel, host=None, port=None):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self.daemon = True
        self.lock = threading.Lock()
        self.broker = Broker()
        self.broker.subscribe(channel)
        self.output = Queue()
        self.channel = channel

    def run(self):
        for source, channel, message in self.broker.listen():
            with self.lock:
                if self._stopevent.isSet():
                    break
                elif channel == self.channel:
                    self.output.put((self._Thread__ident, source, channel, message))

    def stop(self):
        self.broker.stop()
        self._stopevent.set()
        self._Thread__stop()

    def publish(self, source, channel, message):
        self.broker.publish(source, channel, message)


class PubSubMixin(object):
    def GetChannel(self, channel, host=None, port=None, user_id=None):
        if channel not in self.application.channels:
            self.application.channels[channel] = {user_id: PubSub(channel, host, port)}
        elif user_id not in self.application.channels[channel]:
            self.application.channels[channel].update({user_id: PubSub(channel, host, port)})
        else:
            return self.application.channels[channel][user_id]

        self.application.channels[channel][user_id].start()
        return self.application.channels[channel][user_id]


class ClientPubSub(threading.Thread):
    def __init__(self, master, user_id=None):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self.daemon = True
        self.master = master
        self.user_id = user_id

    def run(self):
        while not self._stopevent.isSet():
            try:
                self.master.send_message(*self.master.channel_feed.output.get())
            except tornado.websocket.WebSocketClosedError:
                self.stop()

    def stop(self):
        self._stopevent.set()
        self._Thread__stop()


class WebSocketHandler(tornado.websocket.WebSocketHandler, PubSubMixin):
    def open(self, *args, **kwargs):
        self.channel = kwargs["channel"]
        self.stream.set_nodelay(True)
        self.user_id = uuid.uuid4()

        if self.channel not in clients:
            clients[self.channel] = [self.user_id]
        else:
            clients[self.channel].append(self.user_id)

        self.channel_feed = self.GetChannel(self.channel, user_id=self.user_id)
        self.client_pub_sub = ClientPubSub(self, user_id=self.user_id)
        self.client_pub_sub.start()
        print 'WebSocketHandler - Starting Session with user: %s' % self.user_id
        self.on_connect()

    def on_connect(self):
        from commands import Commands
        message = Commands.user_connected()
        message['data'].update({'threadID': self.channel_feed._Thread__ident})
        self.write_message(message)

    def on_message(self, message):
        # todo - if i want to implement messages from client
        # self.write_message(message)
        pass

    def on_close(self):
        from commands import Commands
        print 'WebSocketHandler - Closing Session for: %s - %s' % (self.channel, self.user_id)
        self.client_pub_sub.stop()
        self.channel_feed.stop()
        if self.channel in clients:
            clients[self.channel].remove(self.user_id)
        try:
            self.write_message(Commands.user_disconnected())
        except tornado.websocket.WebSocketClosedError:
            pass

    def send_message(self, thread_id, source, channel, message):
        print "WebSocketHandler(%s) - Sending message for %s: %s -> %s: %s" % (
            thread_id, self.user_id, source, channel, message)
        # message['data'].update({'source': source, 'threadID': thread_id})
        self.write_message(message)

    def check_origin(self, origin):
        return True


app = tornado.web.Application([
    (r'/ws/(?P<channel>[\w\-\_]*)', WebSocketHandler),
])
app.channels = {}

if __name__ == '__main__':
    parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    app.listen(options.port)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start()
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
