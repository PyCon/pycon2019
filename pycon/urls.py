from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url('program_export/', views.program_export, name='program_export'),
    url(r'^special_event/(?P<slug>.*)/$', views.special_event, name='special_event'),
)
