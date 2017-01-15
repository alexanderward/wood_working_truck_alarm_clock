from django.contrib import admin
from models import Alarm


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_url')


admin.site.register(Alarm, AlarmAdmin)
