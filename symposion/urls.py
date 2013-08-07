from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static

from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

admin.autodiscover()

import symposion.views

# from pinax.apps.account.openid_consumer import PinaxConsumer


URL_PREFIX = settings.CONFERENCE_URL_PREFIXES[settings.CONFERENCE_ID]


urlpatterns = patterns("",
    url(r"^$", RedirectView.as_view(url="/%s/" % URL_PREFIX)),
    url(r"^%s/" % URL_PREFIX, include(patterns("",
        url(r"^$", TemplateView.as_view(template_name="homepage.html"),
            name="home"),
        url(r"^admin/", include(admin.site.urls)),
        url(r"^account/signup/$", symposion.views.SignupView.as_view(), name="account_signup"),
        url(r"^account/login/$", symposion.views.LoginView.as_view(), name="account_login"),
        url(r"^account/social/", include("social_auth.urls")),
        url(r"^account/associations/", include("symposion.social_auth.urls")),
        url(r"^account/", include("account.urls")),
        url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
        url(r"^blog/", include("biblion.urls")),
        url(r"^force500/", lambda request: xxx),

        url(r"^registration/", include("pycon.registration.urls")),

        url(r"^venue/$", TemplateView.as_view(template_name="venue/detail.html"), name="venue_detail"),
        url(r"^venue/traveling/", TemplateView.as_view(template_name="venue/traveling.html"), name="traveling"),
        url(r"^venue/directions/", TemplateView.as_view(template_name="venue/directions.html"), name="directions"),
        url(r"^venue/getting-around/", TemplateView.as_view(template_name="venue/getting_around.html"), name="getting_around"),
        url(r"^venue/weather/", TemplateView.as_view(template_name="venue/weather.html"), name="weather"),
        url(r"^venue/explore/", TemplateView.as_view(template_name="venue/explore.html"), name="explore"),
        url(r"^venue/restaurants/", TemplateView.as_view(template_name="venue/restaurants.html"), name="restaurants"),
        url(r"^venue/bars/", TemplateView.as_view(template_name="venue/bars.html"), name="bars"),
        url(r"^venue/shopping/", TemplateView.as_view(template_name="venue/shopping.html"), name="shopping"),
        url(r"^venue/share-room/", TemplateView.as_view(template_name="venue/share_room.html"), name="share_room"),
        url(r"^venue/hotels/", TemplateView.as_view(template_name="venue/hotels.html"), name="hotels"),

        url(r"^finaid/", include("pycon.finaid.urls")),
        url(r"^pycon_api/", include("pycon.pycon_api.urls")),
        url(r"^schedule/", include("pycon.schedule.urls")),
        url(r"^profile/", include("pycon.profile.urls")),

        url(r"^speaker/", include("symposion.speakers.urls")),
        url(r"^proposals/", include("symposion.proposals.urls")),
        url(r"^reviews/", include("symposion.reviews.urls")),
        url(r"^teams/", include("symposion.teams.urls")),
        url(r"^schedule/", include("symposion.schedule.urls")),
        url(r"^conference/", include("symposion.conference.urls")),

        url(r"^sponsors/", include("pycon.sponsorship.urls")),

        url(r"^boxes/", include("symposion.boxes.urls")),
        url(r"^sitemap/", TemplateView.as_view(template_name="static/sitemap.html"), name="sitemap"),
        url(r'^selectable/', include('selectable.urls')),
        url(r"^", include("symposion.cms.urls")),
    )))
)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
