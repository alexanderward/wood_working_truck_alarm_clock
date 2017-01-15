from alarm_clock.settings import PUBSUB_SERVER_PORT
from enum import Enum

SERVER_PORT = PUBSUB_SERVER_PORT
MAXIMUM_CONNECTIONS = 5
SOCKET_BUFFER_SIZE = 4096
RECONNECT_TIME = 5


class ErrorCodes(Enum):
    InvalidChannelType = 'Channel must be str type.'
    InvalidSocketType = 'Invalid socket type.  Valid types: UDP, TCP'
