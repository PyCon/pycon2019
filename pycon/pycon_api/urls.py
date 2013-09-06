from django.conf.urls import patterns, url
from pycon.pycon_api import views


urlpatterns = patterns("",
    url(r'^proposals/$', views.proposal_list, name='proposal_list'),
    url(r'^proposals/(?P<proposal_id>[\d]+)/$', views.proposal_detail,
        name='proposal_detail',
    ),
    url(r'^proposals/(?P<proposal_id>[\d]+)/logs/$', views.proposal_irc_logs,
        name='proposal_irc_logs',
    )
)
