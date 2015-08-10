from django.conf.urls import patterns, url
from pycon.pycon_api import views


urlpatterns = patterns("",
    url(r'^proposals/$', views.proposal_list, name='proposal_list'),
    url(r'^proposals/(?P<proposal_id>[\d]+)/$', views.proposal_detail,
        name='proposal_detail',
    ),
    url(r'^proposals/(?P<proposal_id>[\d]+)/logs/$', views.proposal_irc_logs,
        name='proposal_irc_logs',
    ),

    url(r'^thunderdome_groups/$', views.thunderdome_group_list, name='thunderdome_groups'),
    url(r'^thunderdome_groups/add/$', views.thunderdome_group_add, name='thunderdome_group_add'),
    url(r'^thunderdome_groups/(?P<td_group_code>[\w\d-]+)/$', views.thunderdome_group_decide,
        name='thunderdome_group_decide'),
)
