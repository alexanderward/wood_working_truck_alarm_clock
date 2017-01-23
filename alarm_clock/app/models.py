from __future__ import unicode_literals
from alarm_clock.settings import PUBSUB_SSE_ALARM_TRUCK_CHANNEL, PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from pubsub.broker import Broker
from sse.commands import Commands
import re

url_regex = re.compile(r'https://www.youtube.com/(\w+)[/\?](.*)')
broker = Broker()


def clean_youtube_link(video):
    youtube_link = url_regex.match(video.url)
    if not youtube_link:
        raise ValidationError("Not a valid YouTube link.")
    video_path = youtube_link.group(2)
    if youtube_link.group(1) == 'watch':
        video_path = video_path.replace('v=', '')
    elif youtube_link.group(1) == 'embed':
        try:
            video_path = video_path[:video_path.index('?')]
        except ValueError:
            pass
    video.url = "https://www.youtube.com/embed/%s?rel=0&autoplay=1" % video_path
    return video


class Video(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        super(Video, self).clean()
        clean_youtube_link(self)


class Alarm(models.Model):
    name = models.CharField(max_length=255, unique=True)
    video = models.ForeignKey(Video, related_name='video')
    time = models.TimeField()
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    last_edited_by = models.IntegerField(null=True)

    def clean(self):
        super(Alarm, self).clean()
        self.video = clean_youtube_link(self.video)

    def save(self, *args, **kwargs):
        def convert_time(message):
            if not isinstance(message['data']['time'], basestring):
                message['data']['time'] = message['data']['time'].strftime("%H:%M:%S")
            return message

        super(Alarm, self).save(*args, **kwargs)
        if 'update_fields' not in kwargs.keys():
            message = Commands.alarm_created(self)
            message = convert_time(message)
            broker.publish(source='app.models.py', channel=PUBSUB_SSE_ALARM_TRUCK_CHANNEL, message=message)
            broker.publish(source='app.models.py', channel=PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL,
                           message=message)
        else:
            message = Commands.alarm_updated(self)
            message = convert_time(message)
            # broker.publish(source='app.models.py', channel=PUBSUB_SSE_ALARM_TRUCK_CHANNEL, message=message)
            broker.publish(source='app.models.py', channel=PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL,
                           message=message)

    def __str__(self):
        return self.name


def alarm_deleted_publish(sender, instance, **kwargs):
    message = Commands.alarm_deleted(instance)
    broker.publish(source='app.models.py', channel=PUBSUB_SSE_ALARM_TRUCK_CONFIGURATION_CHANNEL, message=message)


post_delete.connect(alarm_deleted_publish, sender=Alarm)
