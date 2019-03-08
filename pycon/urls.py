from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url('program_export/', views.program_export, name='program_export'),
    url(r'^events/overview/$', views.scheduled_event_overview, name='scheduled_event_overview'),
    url(r'^event/(?P<slug>.*)/$', views.scheduled_event, name='scheduled_event'),
    url(r'startuprow/apply/$', views.startuprow_apply, name='startuprow_apply'),
    url(r'community/roomsharing/$', views.room_sharing, name='room_sharing'),
    url(r'community/roomsharing/offer/$', views.room_sharing_offer, name='room_sharing_offer'),
    url(r'community/roomsharing/request/$', views.room_sharing_request, name='room_sharing_request'),
    url(r'community/roomsharing/offer/withdraw/$', views.withdraw_room_sharing_offer, name='withdraw_room_sharing_offer'),
    url(r'community/roomsharing/request/withdraw/$', views.withdraw_room_sharing_request, name='withdraw_room_sharing_request'),
    url(r'schedule/edusummits/mini-sprints/$', views.edu_summit_mini_sprints, name="edu_summit_mini_sprints"),

)
