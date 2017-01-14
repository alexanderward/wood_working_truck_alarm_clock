from django.core.exceptions import AppRegistryNotReady
import sys
import os

sys.path.append('..')
try:
    from django.apps import apps

    apps.check_apps_ready()
except AppRegistryNotReady:
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alarm_clock.settings")
    django.setup()

from app.models import Alarm


class Commands(object):
    @staticmethod
    def start_alarm(alarm_name):
        alarm = Alarm.objects.filter(name=alarm_name).first()
        return alarm

    @staticmethod
    def stop_alarm(alarm_name):
        alarm = Alarm.objects.filter(name=alarm_name).first()
        return alarm
