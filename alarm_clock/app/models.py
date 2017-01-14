from __future__ import unicode_literals

from django.db import models


class Alarm(models.Model):
    name = models.CharField(max_length=255, unique=True)
    video_url = models.URLField(null=True, blank=True)
    time = models.TimeField()
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
