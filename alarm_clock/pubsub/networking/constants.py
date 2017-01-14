from enum import Enum

SERVER_PORT = 10000
MAXIMUM_CONNECTIONS = 5
SOCKET_BUFFER_SIZE = 4096


class ErrorCodes(Enum):
    InvalidChannelType = 'Channel must be str type.'
    InvalidSocketType = 'Invalid socket type.  Valid types: UDP, TCP'
