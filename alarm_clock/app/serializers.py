from rest_framework import serializers
from models import Alarm, Video


class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    url = serializers.URLField()

    class Meta:
        model = Video
        field = ('id', 'name', 'url')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.url = validated_data.get('url', instance.url)
        instance.save(update_fields=['name', 'url'])
        try:
            return instance
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def create(self, validated_data):
        try:
            return Video.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))


class AlarmSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    video = VideoSerializer()
    time = serializers.TimeField()
    sunday = serializers.BooleanField()
    monday = serializers.BooleanField()
    tuesday = serializers.BooleanField()
    wednesday = serializers.BooleanField()
    thursday = serializers.BooleanField()
    friday = serializers.BooleanField()
    saturday = serializers.BooleanField()
    enabled = serializers.BooleanField()
    last_edited_by = serializers.IntegerField(allow_null=True)
    flashing_lights = serializers.BooleanField()

    class Meta:
        model = Alarm
        fields = (
            'id', 'name', 'video', 'time', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'enabled', 'last_edited_by', 'flashing_lights')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        video = validated_data.get('video')
        if video:
            instance.video, created = Video.objects.get_or_create(name=video.get("name"), url=video.get('url'))
        instance.time = validated_data.get('time', instance.time)
        instance.sunday = validated_data.get('sunday', instance.sunday)
        instance.monday = validated_data.get('monday', instance.monday)
        instance.tuesday = validated_data.get('tuesday', instance.tuesday)
        instance.wednesday = validated_data.get('wednesday', instance.wednesday)
        instance.thursday = validated_data.get('thursday', instance.thursday)
        instance.friday = validated_data.get('friday', instance.friday)
        instance.saturday = validated_data.get('saturday', instance.saturday)
        instance.enabled = validated_data.get('enabled', instance.enabled)
        instance.last_edited_by = validated_data.get('last_edited_by', instance.enabled)
        instance.flashing_lights = validated_data.get('flashing_lights', instance.flashing_lights)
        try:
            instance.save(
                update_fields=['name', 'video', 'time', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                               'friday', 'saturday', 'enabled', 'last_edited_by', 'flashing_lights'])
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return instance

    def create(self, validated_data):
        video_arg = validated_data.pop('video')
        video, created = Video.objects.get_or_create(name=video_arg.get('name'), url=video_arg.get('url'))
        try:
            return Alarm.objects.create(video=video, **validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))
