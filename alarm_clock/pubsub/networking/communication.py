import sys
import cPickle
import socket
import struct
import logging

marshall = cPickle.dumps
unmarshall = cPickle.loads
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Communication')


class SocketError(Exception):
    def __init__(self, message, error):
        super(SocketError, self).__init__(message)
        self.error = error
        # self.print_error()

    def print_error(self):
        logger.error("%s: %s" % (self.message, str(self.error)))


def send(channel, *args):
    buf = marshall(args)
    value = socket.htonl(len(buf))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buf)


def receive(channel):
    size = struct.calcsize("L")
    try:
        size = channel.recv(size)
    except Exception as e:
        return SocketError("Pubsub -> Networking -> Communication -> receive", e)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error, e:
        return SocketError("Pubsub -> Networking -> Communication -> receive", e)

    buf = ""

    while len(buf) < size:
        buf = channel.recv(size - len(buf))

    try:
        return unmarshall(buf)[0]
    except TypeError:
        pass
    except Exception as e:
        return SocketError("Pubsub -> Networking -> Communication -> receive", e)
