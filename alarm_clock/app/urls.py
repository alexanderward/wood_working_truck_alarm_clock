from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'test-alarm/$', views.test_alarm, name='test_alarm'),
    url(r'test-alarm/(?P<alarm_id>\d+)/$', views.test_alarm, name='test_alarm'),
    url(r'^', views.index, name='index'),
]
