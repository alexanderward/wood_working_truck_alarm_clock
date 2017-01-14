import Queue
import json

import collections

from pubsub.networking.constants import ErrorCodes
from pubsub.networking.client import Client


class Broker(object):
    __channels = list()
    __queue = Queue.Queue()
    client = None

    def __init__(self):
        self.setup_client()

    def setup_client(self):
        self.client = Client()
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
        response = json.loads(response)
        channel = response['channel']
        source = response['source']
        msg = self.normalize_json(response['msg'])
        self.__queue.put((source, channel, msg))

    def listen(self):
        self.client.start_receive()
        while 1:
            while not self.__queue.empty():
                source, channel, msg = self.__queue.get()
                if channel in self.channels:
                    yield (source, channel, msg)
