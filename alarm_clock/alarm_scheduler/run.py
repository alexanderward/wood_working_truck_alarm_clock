import time

import datetime

from alarm_clock.settings import PUBSUB_SSE_CHANNEL
import threading
import os, sys
from django.core.exceptions import AppRegistryNotReady
from sse.run import PubSub

sys.path.append('..')
try:
    from django.apps import apps

    apps.check_apps_ready()
except AppRegistryNotReady:
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alarm_clock.settings")
    django.setup()
from app.models import Alarm


class PubSubMonitor(threading.Thread):
    def __init__(self, master, channel):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self.daemon = True
        self.master = master
        self.channel = channel

    def run(self):
        while not self._stopevent.isSet():
            thread_id, source, channel, message = self.master.pubsub.output.get()
            print thread_id, source, channel, message
            if channel == self.channel and message.get('event', None) == 'alarmCreated':
                self.master.alarms = self.master.convert_queryset_to_day_dict(Alarm.objects.all())

    def stop(self):
        self._stopevent.set()
        self._Thread__stop()


class Scheduler(object):
    def __init__(self):
        self.channel = PUBSUB_SSE_CHANNEL
        self.alarms = self.convert_queryset_to_day_dict(Alarm.objects.all())
        self.pubsub = PubSub(self.channel)
        self.pubsub_monitor = PubSubMonitor(self, self.channel)

    def convert_queryset_to_day_dict(self, alarm_queryset):
        return {
            0: alarm_queryset.filter(monday=True),
            1: alarm_queryset.filter(tuesday=True),
            2: alarm_queryset.filter(wednesday=True),
            3: alarm_queryset.filter(thursday=True),
            4: alarm_queryset.filter(friday=True),
            5: alarm_queryset.filter(saturday=True),
            6: alarm_queryset.filter(sunday=True)
        }

    def run(self):
        from sse.commands import Commands
        self.pubsub.start()
        self.pubsub_monitor.start()

        executing_this_alarm_this_minute = None
        while 1:
            now = datetime.datetime.now()
            current_day = now.weekday()
            now_tuple = (now.hour, now.minute)
            if executing_this_alarm_this_minute != now_tuple:
                for alarm in self.alarms[current_day].filter(enabled=True):
                    if now_tuple == (alarm.time.hour, alarm.time.minute):
                        self.pubsub.publish(source='alarm_scheduler.run', channel=self.channel,
                                            message=Commands.start_alarm(alarm))
                        executing_this_alarm_this_minute = now_tuple
                        print '[%s] %s - %s' % (now, alarm.name, alarm.video_url)
                        break
            time.sleep(1)


if __name__ == '__main__':
    Scheduler().run()
