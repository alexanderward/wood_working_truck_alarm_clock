import signal

import datetime
import time
from Queue import Queue

import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
import sys
from commands import Commands

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


def get_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


class PubSub(threading.Thread):
    def __init__(self, channel, host=None, port=None):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.broker = Broker()
        self.broker.subscribe(channel)
        self.output = Queue()

    def run(self):
        for source, channel, message in self.broker.listen():
            with self.lock:
                self.output.put((source, channel, message))

    def stop(self):
        self._Thread__stop()


class PubSubMixin(object):
    def GetChannel(self, channel, host=None, port=None):
        if channel not in self.application.channels:
            self.application.channels[channel] = PubSub(channel, host, port)
            self.application.channels[channel].start()
        return self.application.channels[channel]


class ClientPubSub(threading.Thread):
    def __init__(self, master):
        super(ClientPubSub, self).__init__()
        self.master = master
        self.running = True

    def run(self):
        while self.running:
            try:
                self.master.send_message(*self.master.channel_feed.output.get())
            except tornado.websocket.WebSocketClosedError:
                self.stop()

    def stop(self):
        self.running = False
        self._Thread__stop()


class WebSocketHandler(tornado.websocket.WebSocketHandler, PubSubMixin):
    def open(self, *args, **kwargs):
        self.channel = kwargs["channel"]
        self.stream.set_nodelay(True)
        clients[self.channel] = {"id": self.channel, "object": self}
        self.channel_feed = self.GetChannel(self.channel)
        self.client_pub_sub = ClientPubSub(self).start()

    def on_message(self, message):
        print "Client %s received a message: %s" % (self.channel, message)
        self.write_message("[%s] - Client id: %s" % (get_timestamp(), self.channel,))

    def on_close(self):
        if self.channel in clients:
            del clients[self.channel]
        try:
            self.write_message("[%s] - Closing for session Client id: %s" % (get_timestamp(), self.channel,))
        except tornado.websocket.WebSocketClosedError:
            pass

    def send_message(self, source, channel, message):
        self.write_message("%s -> %s: %s" % (source, channel, message))

    def check_origin(self, origin):
        return True


app = tornado.web.Application([
    (r'/ws/(?P<channel>\w*)', WebSocketHandler),
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
