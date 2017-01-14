import socket
import sys
import logging
from communication import send, receive
from constants import SERVER_PORT
import threading


def try_connect(function):
    def try_fn(self, *args, **kwargs):
        try:
            function(self, *args, **kwargs)
        except socket.error, e:
            self.logger.error('Could not connect to chat server')
            sys.exit(1)

    return try_fn


class Client(object):
    __server_port = SERVER_PORT
    __server_address = ('localhost', __server_port)
    __callbackFn = None
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('Server')

    def __init__(self):
        self.setup_socket()

    @try_connect
    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.__server_address)

    def start_receive(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.daemon = True
        listen_thread.start()

    @property
    def callbackFn(self):
        return self.__callbackFn

    @callbackFn.setter
    def callbackFn(self, callbackFn):
        self.__callbackFn = callbackFn

    @try_connect
    def send(self, message):
        send(self.sock, message)

    @try_connect
    def listen(self):
        while 1:
            data = receive(self.sock)
            if self.callbackFn:
                self.callbackFn(data)
            else:
                self.logger.info('Recieved: %s' % data)
