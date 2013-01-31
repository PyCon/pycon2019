from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static

from django.views.generic.simple import direct_to_template, redirect_to

from django.contrib import admin
admin.autodiscover()

import symposion.views

# from pinax.apps.account.openid_consumer import PinaxConsumer


URL_PREFIX = settings.CONFERENCE_URL_PREFIXES[settings.CONFERENCE_ID]


urlpatterns = patterns("",
    url(r"^$", redirect_to, {"url": "/%s/" % URL_PREFIX}),
    url(r"^%s/" % URL_PREFIX, include(patterns("",
        url(r"^$", direct_to_template, {
            "template": "homepage.html",
        }, name="home"),
        url(r"^admin/", include(admin.site.urls)),
        url(r"^account/signup/$", symposion.views.SignupView.as_view(), name="account_signup"),
        url(r"^account/login/$", symposion.views.LoginView.as_view(), name="account_login"),
        url(r"^account/social/", include("social_auth.urls")),
        url(r"^account/associations/", include("symposion.social_auth.urls")),
        url(r"^account/", include("account.urls")),
        url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
        url(r"^markitup/", include("markitup.urls")),
        url(r"^blog/", include("biblion.urls")),
        url(r"^force500/", lambda request: xxx),
        
        url(r"^registration/", include("pycon.registration.urls")),
        
        #temp
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
        url(r"^venue/hotels/", direct_to_template, {"template": "venue/hotels.html"}, name="hotels"),
        
        url(r"^schedule/", include("pycon.schedule.urls")),
        
        url(r"^speaker/", include("symposion.speakers.urls")),
        url(r"^proposals/", include("symposion.proposals.urls")),
        url(r"^reviews/", include("symposion.reviews.urls")),
        url(r"^teams/", include("symposion.teams.urls")),
        url(r"^schedule/", include("symposion.schedule.urls")),
        url(r"^conference/", include("symposion.conference.urls")),
        
        url(r"^sponsors/", include("pycon.sponsorship.urls")),
        
        url(r"^boxes/", include("symposion.boxes.urls")),
        url(r"^sitemap/", direct_to_template, { "template": "static/sitemap.html", }, name="sitemap"),
        url(r"^", include("symposion.cms.urls")),
    )))
)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)