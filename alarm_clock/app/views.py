from alarm_clock.settings import SSE_PORT, PUBSUB_SSE_CHANNEL
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', context={'sse_port': SSE_PORT, 'sse_channel': PUBSUB_SSE_CHANNEL})
