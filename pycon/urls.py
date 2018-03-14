from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url('program_export/', views.program_export, name='program_export'),
    url(r'^events/overview/$', views.scheduled_event_overview, name='scheduled_event_overview'),
    url(r'^event/(?P<slug>.*)/$', views.scheduled_event, name='scheduled_event'),
)
