from rest_framework import serializers
from models import Alarm


class AlarmSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    video_url = serializers.URLField()
    time = serializers.TimeField()
    sunday = serializers.BooleanField()
    monday = serializers.BooleanField()
    tuesday = serializers.BooleanField()
    wednesday = serializers.BooleanField()
    thursday = serializers.BooleanField()
    friday = serializers.BooleanField()
    saturday = serializers.BooleanField()

    class Meta:
        model = Alarm
        fields = '__all__'
