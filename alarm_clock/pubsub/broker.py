import Queue
import json

import collections

from pubsub.networking.constants import ErrorCodes
from pubsub.networking.client import Client
import logging

class Broker(object):
    __channels = list()
    __queue = Queue.Queue()
    client = None
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('Broker')

    def __init__(self):
        self.__continue = True
        self.setup_client()

    def setup_client(self):
        self.client = Client(master=self)
        self.client.callbackFn = self.format_response

    @property
    def channels(self):
        return self.__channels

    def subscribe(self, channel):
        if isinstance(channel, basestring):
            self.__channels.append(channel)
        else:
            raise ValueError(ErrorCodes.InvalidChannelType.value)

    def unsubscribe(self, channel):
        if channel in self.__channels:
            self.__channels.remove(channel)

    def stop(self):
        my_ip, my_port = self.client.sock.getsockname()
        peer_ip, peer_port = self.client.sock.getpeername()
        self.logger.info('Broker -> Stop: %s:%s - %s: %s' % (my_ip, my_port, peer_ip, peer_port))
        self.__continue = False
        self.client.exit()

    def publish(self, source, channel, message):
        if not isinstance(channel, basestring) or not isinstance(source, basestring):
            raise ValueError(ErrorCodes.InvalidChannelType.value)

        message = json.dumps({'msg': message, 'channel': channel, 'source': source})
        self.client.send(message)

    def normalize_json(self, data):
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(self.normalize_json, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self.normalize_json, data))
        else:
            return data

    def format_response(self, response):
        if response:
            response = json.loads(response)
            channel = response['channel']
            source = response['source']
            msg = self.normalize_json(response['msg'])
            self.__queue.put((source, channel, msg))

    def listen(self):
        self.client.start_receive()
        while self.__continue:
            while not self.__queue.empty():
                source, channel, msg = self.__queue.get()
                if channel in self.channels:
                    yield (source, channel, msg)
