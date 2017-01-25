from app.views import PartialGroupView
from django.conf.urls import include, url
from . import views

partial_patterns = [
    url(r'^home.html$', PartialGroupView.as_view(template_name='partials/home.html'), name='home'),
    url(r'^new-alarm.html$', PartialGroupView.as_view(template_name='partials/new-alarm.html'), name='new_alarm'),
]

urlpatterns = [
    url(r'test-alarm/$', views.test_alarm, name='test_alarm'),
    url(r'test-alarm/(?P<alarm_id>\d+)/$', views.test_alarm, name='test_alarm'),
    url(r'configure/$', views.configure, name='configure'),
    url(r'^partials/', include(partial_patterns, namespace='partials')),
    url(r'^', views.index, name='index'),
]
