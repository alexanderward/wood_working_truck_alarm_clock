from __future__ import unicode_literals
from alarm_clock.settings import PUBSUB_SSE_CHANNEL
from django.db import models
from pubsub.broker import Broker
from sse.commands import Commands
from datetime import datetime
broker = Broker()


class Video(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


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

    def save(self, *args, **kwargs):
        super(Alarm, self).save(*args, **kwargs)
        message = Commands.alarm_created(self)
        if not isinstance(message['alarm']['time'], basestring):
            message['alarm']['time'] = message['alarm']['time'].strftime("%H:%M:%S")
        broker.publish(source='app.models.py', channel=PUBSUB_SSE_CHANNEL, message=message)

    def __str__(self):
        return self.name
