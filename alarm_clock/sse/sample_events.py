import time

from alarm_clock.settings import PUBSUB_SSE_CHANNEL
from pubsub.broker import Broker
from commands import Commands
if __name__ == '__main__':
    broker = Broker()
    counter = 1
    # message = Commands.start_alarm('Test Alarm')
    message = Commands.start_alarm('Paw Patrol')
    broker.publish(source='sample_events.py', channel=PUBSUB_SSE_CHANNEL, message=message)
    # while 1:
    #     message = Commands.start_alarm('Test Alarm')
    #     broker.publish(source='sample_events.py', channel=PUBSUB_SSE_CHANNEL, message=message)
    #     counter += 1
    #     time.sleep(60)
