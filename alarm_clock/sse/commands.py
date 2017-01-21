from django.core.exceptions import AppRegistryNotReady
import sys
import os
from django.forms.models import model_to_dict
import datetime
import time

sys.path.append('..')
try:
    from django.apps import apps

    apps.check_apps_ready()
except AppRegistryNotReady:
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alarm_clock.settings")
    django.setup()

def get_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


class Commands(object):
    @staticmethod
    def __get_alarm(alarm_name):
        from app.models import Alarm
        alarm = None
        if isinstance(alarm_name, str):
            alarm = Alarm.objects.filter(name=alarm_name).first()
        elif isinstance(alarm_name, Alarm):
            alarm = alarm_name
        return alarm

    @staticmethod
    def start_alarm(alarm_name):
        from app.serializers import AlarmSerializer
        alarm = Commands.__get_alarm(alarm_name)
        if alarm:
            return {'event': 'startAlarm',
                    'alarm': AlarmSerializer(alarm).data}

    @staticmethod
    def stop_alarm(alarm_name=None):
        from app.serializers import AlarmSerializer
        if alarm_name is None:
            alarm = 'Broadcast Stop'
        else:
            alarm = Commands.__get_alarm(alarm_name)
            alarm = AlarmSerializer(alarm).data
        if alarm:
            return {'event': 'stopAlarm',
                    'alarm': alarm}

    @staticmethod
    def alarm_created(alarm_name):
        from app.serializers import AlarmSerializer
        alarm = Commands.__get_alarm(alarm_name)
        return {'event': 'alarmCreated',
                'alarm': AlarmSerializer(alarm).data}

    @staticmethod
    def user_connected():
        return {'event': 'userConnected', 'message': "[%s] - Connected" % get_timestamp()}

    @staticmethod
    def user_disconnected():
        return {'event': 'userDisconnected', 'message': "[%s] - Disconnected" % get_timestamp()}
