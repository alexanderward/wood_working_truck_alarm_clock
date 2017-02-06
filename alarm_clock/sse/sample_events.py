import time

from alarm_clock.settings import PUBSUB_SSE_ALARM_TRUCK_CHANNEL, PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL
from pubsub.broker import Broker
from commands import Commands

if __name__ == '__main__':
    broker = Broker()
    counter = 1
    # message = Commands.start_alarm('Test Alarm')
    message = Commands.start_alarm('Daniel2')
    # message = Commands.start_alarm('Peaches')
    broker.publish(source='sample_events.py', channel=PUBSUB_SSE_ALARM_TRUCK_CHANNEL, message=message)
    # broker.publish(source='sample_events.py', channel=PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL, message={'event': 'test', 'data': 'keke'})
    # broker.publish(source='sample_events.py', channel=PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL,
    #                message={'event': 'alarmDeleted',
    #                         'data': {'name': 'test', 'monday': False, 'tuesday': False, 'friday': False,
    #                                  'enabled': True, 'wednesday': False, 'thursday': False, 'id': 24, 'sunday': False,
    #                                  'video': {'url': 'https://www.youtube.com/embed/93FprsmspCs?rel=0&autoplay=1',
    #                                            'id': 1, 'name': 'Walking Dead'}, 'time': '16:27:03', 'saturday': False}
    #                         })
    # while 1:
    #     message = Commands.start_alarm('Test Alarm')
    #     broker.publish(source='sample_events.py', channel=PUBSUB_SSE_ALARM_TRUCK_CHANNEL, message=message)
    #     counter += 1
    #     time.sleep(60)
