from alarm_clock.settings import SSE_PORT, PUBSUB_SSE_CHANNEL
from django.http import JsonResponse
from django.shortcuts import render
from pubsub.broker import Broker
from rest_framework import viewsets
from models import Alarm
from serializers import AlarmSerializer
from django.forms.models import model_to_dict
from sse.commands import Commands

broker = Broker()


def index(request):
    return render(request, 'index.html', context={'sse_port': SSE_PORT, 'sse_channel': PUBSUB_SSE_CHANNEL})


def test_alarm(request, alarm_id=None):
    alarm = Alarm.objects.filter(pk=alarm_id).first()
    obj = {}
    error_msg = None
    if not alarm and alarm is not None:
        obj = {'error': 'Not a valid id for any alarm!'}
    elif request.method == 'GET':
        obj = model_to_dict(alarm)
    elif request.method == 'POST':
        event = request.POST.get('event')
        if event == 'start':
            try:
                status = 'success'
                message = Commands.start_alarm(alarm)
                broker.publish(source='app.views.test_alarm.POST', channel=PUBSUB_SSE_CHANNEL, message=message)
            except Exception as e:
                status = 'failed'
                error_msg = str(e)
        elif event == 'stop':
            try:
                status = 'success'
                message = Commands.stop_alarm(alarm)
                broker.publish(source='app.views.test_alarm.POST', channel=PUBSUB_SSE_CHANNEL, message=message)
            except Exception as e:
                status = 'failed'
                error_msg = str(e)
        else:
            status = 'unknown event'
        obj = {'event': event, 'status': status, 'alarm': 'Broadcast Stop' if not alarm else model_to_dict(alarm)}
        if error_msg:
            obj.update({'error_msg': error_msg})

    return JsonResponse(obj, safe=False)


class AlarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows alarms to be viewed or edited.
    """
    queryset = Alarm.objects.all().order_by('pk')
    serializer_class = AlarmSerializer
