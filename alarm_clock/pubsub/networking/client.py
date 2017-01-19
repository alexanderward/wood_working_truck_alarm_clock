import socket
import sys
import logging
from communication import send, receive, SocketError
from constants import SERVER_PORT, RECONNECT_TIME
import threading
import time

current_tries = 0
total_tries = 10


def try_connect(function):
    def try_fn(self, *args, **kwargs):
        try:
            function(self, *args, **kwargs)
        except socket.error, e:
            self.logger.error('Could not connect to server')
            self.sock.close()
            time.sleep(RECONNECT_TIME)
            global current_tries
            global total_tries
            if current_tries < total_tries:
                current_tries += 1
                self.logger.error('Reconnecting to server')
                self.setup_socket()
                function(self, *args, **kwargs)
                # sys.exit(1)

    return try_fn


class Client(object):
    __server_port = SERVER_PORT
    __server_address = ('localhost', __server_port)
    __callbackFn = None
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('Server')

    def __init__(self, master=None):
        self.setup_socket()
        self.__continue = True
        self.master = master

    # @try_connect
    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.__server_address)
        server_ip, server_port = self.sock.getpeername()
        client_ip, client_port = self.sock.getsockname()
        self.logger.info("Connected to server (%s:%s) as %s:%s" % (server_ip, server_port, client_ip, client_port))

    def start_receive(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.daemon = True
        listen_thread.start()

    def exit(self):
        self.__continue = False
        my_ip, my_port = self.sock.getsockname()
        peer_ip, peer_port = self.sock.getpeername()
        self.sock.shutdown(1)
        self.logger.info('Client -> Exit: %s:%s - %s: %s' % (my_ip, my_port, peer_ip, peer_port))

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
        while self.__continue:
            data = receive(self.sock)
            if isinstance(data, SocketError):
                break
            if self.callbackFn:
                self.callbackFn(data)
            else:
                self.logger.info('Received: %s' % data)
        if self.master:
            self.master.stop()
        else:
            self.exit()
