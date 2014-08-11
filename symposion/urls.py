from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static

from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

import symposion.views


admin.autodiscover()

URL_PREFIX = settings.CONFERENCE_URL_PREFIXES[settings.CONFERENCE_ID]


urlpatterns = patterns(
    "",
    url(r"^$", RedirectView.as_view(url="/%s/" % URL_PREFIX)),
    url(r"^%s/" % URL_PREFIX, include(patterns(
        "",
        url(r"^$",
            TemplateView.as_view(template_name="homepage.html"),
            name="home"),
        url(r"^dashboard/$",
            symposion.views.dashboard,
            name="dashboard"),
        url(r"^sitemap/$",
            TemplateView.as_view(template_name="static/sitemap.html"),
            name="sitemap"),
        url(r"^change_language/$",
            symposion.views.change_language,
            name="change_language"),
        url(r"^force500/$", lambda request: xxx),

        # Accounts.
        url(r"^account/signup/$",
            symposion.views.SignupView.as_view(),
            name="account_signup"),
        url(r"^account/login/$",
            symposion.views.LoginView.as_view(),
            name="account_login"),
        url(r"^account/associations/", include("symposion.social_auth.urls")),
        url(r"^account/social/", include("social_auth.urls")),
        url(r"^account/", include("account.urls")),

        url(r"^admin/", include(admin.site.urls)),
        url(r"^blog/", include("biblion.urls")),
        url(r"^boxes/", include("symposion.boxes.urls")),
        url(r"^conference/", include("symposion.conference.urls")),
        url(r"^finaid/", include("pycon.finaid.urls")),
        url(r"^profile/", include("pycon.profile.urls")),
        url(r"^proposals/", include("symposion.proposals.urls")),
        url(r"^pycon_api/", include("pycon.pycon_api.urls")),
        url(r"^registration/", include("pycon.registration.urls")),
        url(r"^reviews/", include("symposion.reviews.urls")),
        url(r"^schedule/", include("pycon.schedule.urls")),
        url(r"^schedule/", include("symposion.schedule.urls")),
        url(r"^selectable/", include("selectable.urls")),
        url(r"^speaker/", include("symposion.speakers.urls")),
        url(r"^sponsors/", include("pycon.sponsorship.urls")),
        url(r"^teams/", include("symposion.teams.urls")),
        url(r"^tutorials/", include("pycon.tutorials.urls")),

        url(r"^", include("pycon.urls")),

        # This should be last, because it will create a new CMS page for
        # any unrecognized URL.
        url(r"^", include("symposion.cms.urls")),
    )))
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "comps" in settings.INSTALLED_APPS:
    urlpatterns += patterns("", url(r"^", include("comps.urls")))
