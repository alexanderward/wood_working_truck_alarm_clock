import signal

import datetime
import time
import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
import sys

sys.path.append('..')
from alarm_clock.settings import SSE_PORT
from tornado.options import define, options, parse_command_line

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


class Main(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    def get(self, **kwargs):
        if "Id" in kwargs.keys():
            print "Your client id is: %s" % (kwargs["Id"],)
        self.write("This is your response")
        self.finish()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self, *args, **kwargs):
        self.id = kwargs["Id"]
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):
        print "Client %s received a message: %s" % (self.id, message)
        self.write_message("[%s] - Client id: %s" % (get_timestamp(), self.id,))

    def on_close(self):
        self.write_message("[%s] - Closing for session Client id: %s" % (get_timestamp(), self.id,))
        if self.id in clients:
            del clients[self.id]

    def check_origin(self, origin):
        return True


app = tornado.web.Application([
    (r'/', Main),
    (r'/ws/(?P<Id>\w*)', WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    app.listen(options.port)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()
