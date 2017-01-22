import time

from alarm_clock.settings import PUBSUB_SSE_ALARM_TRUCK_CHANNEL, PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL
from pubsub.broker import Broker
from commands import Commands
if __name__ == '__main__':
    broker = Broker()
    counter = 1
    # message = Commands.start_alarm('Test Alarm')
    message = Commands.start_alarm('Paw Patrol')
    # message = Commands.start_alarm('Peaches')
    broker.publish(source='sample_events.py', channel=PUBSUB_SSE_ALARM_TRUCK_CHANNEL, message=message)
    broker.publish(source='sample_events.py', channel=PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL, message={'test': 'yay'})
    # while 1:
    #     message = Commands.start_alarm('Test Alarm')
    #     broker.publish(source='sample_events.py', channel=PUBSUB_SSE_ALARM_TRUCK_CHANNEL, message=message)
    #     counter += 1
    #     time.sleep(60)
