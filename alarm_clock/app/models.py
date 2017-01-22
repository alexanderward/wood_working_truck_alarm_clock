from __future__ import unicode_literals
from alarm_clock.settings import PUBSUB_SSE_ALARM_TRUCK_CHANNEL
from django.core.exceptions import ValidationError
from django.db import models
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

    def clean(self):
        super(Alarm, self).clean()
        self.video = clean_youtube_link(self.video)

    def save(self, *args, **kwargs):
        super(Alarm, self).save(*args, **kwargs)
        message = Commands.alarm_created(self)
        if not isinstance(message['alarm']['time'], basestring):
            message['alarm']['time'] = message['alarm']['time'].strftime("%H:%M:%S")
        broker.publish(source='app.models.py', channel=PUBSUB_SSE_ALARM_TRUCK_CHANNEL, message=message)

    def __str__(self):
        return self.name
