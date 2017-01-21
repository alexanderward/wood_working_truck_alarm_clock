from alarm_clock.settings import SSE_PORT, PUBSUB_SSE_CHANNEL
from django.http import JsonResponse
from django.shortcuts import render
from pubsub.broker import Broker
from rest_framework import status, viewsets
from models import Alarm, Video
from serializers import AlarmSerializer, VideoSerializer
from django.forms.models import model_to_dict
from sse.commands import Commands
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

broker = Broker()


class GenericViewSet(viewsets.ModelViewSet):
    def list(self, request, **kwargs):
        queryset = self.queryset
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        return JSONResponse(serializer.data)

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.create(serializer.data)
            response_serializer = self.get_serializer(instance)
            return JSONResponse(response_serializer.data)
        else:
            return JSONResponse(serializer.errors)

    def retrieve(self, request, pk=None, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return JSONResponse(serializer.data)
        else:
            return JSONResponse(None)

    def update(self, request, pk=None, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.update(instance, serializer.data)
                serializer = self.get_serializer(instance)
                return JSONResponse(serializer.data)
            else:
                return JSONResponse(serializer.errors)

    def destroy(self, request, pk=None, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JSONResponse({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        if data is None:
            data = {'error': 'No records found.'}
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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


class AlarmViewSet(GenericViewSet):
    """
    API endpoint that allows Alarms to be viewed or edited.
    """

    serializer_class = AlarmSerializer
    queryset = Alarm.objects.all()

    def __init__(self, **kwargs):
        super(AlarmViewSet, self).__init__(**kwargs)


class VideoViewSet(GenericViewSet):
    """
    API endpoint that allows Alarms to be viewed or edited.
    """

    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def __init__(self, **kwargs):
        super(VideoViewSet, self).__init__(**kwargs)
