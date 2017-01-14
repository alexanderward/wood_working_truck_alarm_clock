import time

from pubsub.broker import Broker
from commands import Commands
if __name__ == '__main__':
    broker = Broker()
    counter = 1
    while 1:
        message = {'webserver': Commands.start_alarm('test')}
        broker.publish(source='sample_events.py', channel='test', message=message)
        counter += 1
        time.sleep(5)
