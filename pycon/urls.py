from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url('program_export/', views.program_export, name='program_export'),
    url(r'^event/(?P<slug>.*)/$', views.scheduled_event, name='scheduled_event'),
)
