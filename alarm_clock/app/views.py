from alarm_clock.settings import SSE_PORT
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', context={'sse_port': SSE_PORT})
