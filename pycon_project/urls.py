from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer

from pycon_project.views import creole_preview


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", redirect_to, {"url": "/%s/"  % settings.PYCON_YEAR}),
    url(r"^%s/" % settings.PYCON_YEAR, include(patterns("",
        url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
        url(r"^account/signup/$", "pinax.apps.account.views.signup", name="acct_signup"),
        url(r"^account/", include("pinax.apps.account.urls")),
        url(r"^openid/", include(PinaxConsumer().urls)),
        # url(r"^oauth_access/finish_signup/(?P<service>\w+)/$", "oauth_callbacks.finish_signup", name="oauth_access_finish_signup"),
        # url(r"^oauth_access/", include("oauth_access.urls")),
        url(r"^blog/", include("biblion.urls")),
        url(r"^speaker/", include("speakers.urls")),
        url(r"^proposal/", include("proposals.urls")),
        url(r"^review/", include("review.urls")),
        url(r"^waitinglist/", include("pinax.apps.waitinglist.urls")),
        url(r"^schedule/", include("schedule.urls")),
        url(r"^user_mailer/", include("user_mailer.urls")),
        url(r"^sponsors/", include("sponsors.urls")),
        url(r"^admin/", include(admin.site.urls)),
        url(r"^creole_preview/$", creole_preview, name="creole_preview"),
        url(r"^feed/(?P<section>\w+)/$", "biblion.views.blog_feed", name="blog_feed"),
        url(r"^markitup/", include("markitup.urls")),
        url(r"^export_data/speakers\.txt$", "schedule.views.schedule_export_speaker_data"),
        url(r"^export_data/sponsors\.txt$", "sponsors.views.sponsor_export_data"),
        url(r"^venue/", direct_to_template, {"template": "venue/detail.html"}, name="venue_detail"),
        url(r"^export_data/panels\.txt$", "schedule.views.schedule_export_panels"),
        url(r"^", include("wakawaka.urls")),
    ))),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"^favicon.ico$", redirect_to, {
            "url": settings.STATIC_URL + "img/favicon.ico",
        }),
        url(r"", include("staticfiles.urls")),
    )
