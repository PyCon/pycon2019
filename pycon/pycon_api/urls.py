from django.conf.urls import patterns, url

from .views import get_proposal_data, set_proposal_data, \
    get_irc_logs, set_irc_logs


urlpatterns = patterns("",
    url(r"^get_proposal_data/(?P<auth_key>[0-9a-z-]{36})/(?P<proposal_id>\d+)/$",
        get_proposal_data, name="get_proposal_data"),
    url(r"^set_proposal_data/(?P<auth_key>[0-9a-z-]{36})/(?P<proposal_id>\d+)/$",
        set_proposal_data, name="set_proposal_data"),
    url(r"^get_irc_logs/(?P<auth_key>[0-9a-z-]{36})/(?P<proposal_id>\d+)/$",
        get_irc_logs, name="get_irc_logs"),
    url(r"^set_irc_logs/(?P<auth_key>[0-9a-z-]{36})/$",
        set_irc_logs, name="set_irc_logs"),
)
