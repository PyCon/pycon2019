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
        url(r"^waitinglist/", include("pinax.apps.waitinglist.urls")),
        url(r"^mailout/", include("mailout.urls")),
        
        url(r"^admin/", include(admin.site.urls)),
        url(r"^creole_preview/$", creole_preview, name="creole_preview"),
        url(r"^feed/(?P<section>\w+)/$", "biblion.views.blog_feed", name="blog_feed"),
        url(r"^markitup/", include("markitup.urls")),
        
        # Symposion Apps
        url(r"^speaker/", include("symposion.speakers.urls")),
        url(r"^proposal/", include("symposion.proposals.urls")),
        url(r"^review/", include("symposion.review.urls")),
        url(r"^sponsors/", include("symposion.sponsors_pro.urls")),

        url(r"^schedule/lists/(\w+)/$", "symposion.schedule.views.schedule_presentation_list", name="schedule_presentation_list"),
        url(r"^schedule/presentation/(\d+)/$", "symposion.schedule.views.schedule_presentation", name="schedule_presentation"),

        # url(r"^schedule/", include("symposion.schedule.urls")),
        # url(r"^export_data/speakers\.txt$", "schedule.views.schedule_export_speaker_data"),
        # url(r"^export_data/sponsors\.txt$", "sponsors.views.sponsor_export_data"),
        # url(r"^export_data/panels\.txt$", "schedule.views.schedule_export_panels"),
        
        url(r"^about/$", direct_to_template, {"template": "pycon/about.html"}, name="about"),
        url(r"^venue/$", direct_to_template, {"template": "venue/detail.html"}, name="venue_detail"),
        url(r"^venue/traveling/", direct_to_template, {"template": "venue/traveling.html"}, name="traveling"),
        url(r"^venue/directions/", direct_to_template, {"template": "venue/directions.html"}, name="directions"),
        url(r"^venue/getting-around/", direct_to_template, {"template": "venue/getting_around.html"}, name="getting_around"),
        url(r"^venue/weather/", direct_to_template, {"template": "venue/weather.html"}, name="weather"),
        url(r"^venue/explore/", direct_to_template, {"template": "venue/explore.html"}, name="explore"),
        url(r"^venue/restaurants/", direct_to_template, {"template": "venue/restaurants.html"}, name="restaurants"),
        url(r"^venue/bars/", direct_to_template, {"template": "venue/bars.html"}, name="bars"),
        url(r"^venue/shopping/", direct_to_template, {"template": "venue/shopping.html"}, name="shopping"),
        url(r"^venue/share-room/", direct_to_template, {"template": "venue/share_room.html"}, name="share_room"),
        
        url(r"^registration/", include("registration.urls")),
        url(r"^boxes/", include("boxes.urls")),
        
        url(r"^", include("wakawaka.urls")),
    ))),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"^favicon.ico$", redirect_to, {
            "url": settings.STATIC_URL + "img/favicon.ico",
        }),
        url(r"^%s/site_media/media/(?P<path>.*)$" % settings.PYCON_YEAR, "django.views.static.serve", {
            "document_root": settings.MEDIA_ROOT,
        }),
        url(r"", include("staticfiles.urls")),
    )
