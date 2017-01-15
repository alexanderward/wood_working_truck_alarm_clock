from alarm_clock.settings import SSE_PORT, PUBSUB_SSE_CHANNEL
from django.shortcuts import render
from rest_framework import viewsets
from models import Alarm
from serializers import AlarmSerializer


def index(request):
    return render(request, 'index.html', context={'sse_port': SSE_PORT, 'sse_channel': PUBSUB_SSE_CHANNEL})


class AlarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows alarms to be viewed or edited.
    """
    queryset = Alarm.objects.all().order_by('pk')
    serializer_class = AlarmSerializer
