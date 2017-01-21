from django.contrib import admin
from models import Alarm, Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('name',)# 'get_video_name')

    # def get_video_name(self, obj):
    #     return str(obj.video.name)

    # def get_video_name(self, obj):
    #     return str(obj.video.name)

    # get_video_name.admin_order_field = 'url'  # Allows column order sorting
    # get_name.short_description = 'Author Name'  # Renames column head

admin.site.register(Alarm, AlarmAdmin)
admin.site.register(Video, VideoAdmin)
