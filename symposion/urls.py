from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

import symposion.views

# from pinax.apps.account.openid_consumer import PinaxConsumer


PAGE_RE = settings.SYMPOSION_PAGE_REGEX

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("symposion.about.urls")),
    url(r"^account/signup/$", symposion.views.SignupView.as_view(), name="account_signup"),
    url(r"^account/login/$", symposion.views.LoginView.as_view(), name="account_login"),
    url(r"^account/", include("account.urls")),
    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
    url(r"^markitup/", include("markitup.urls")),
    url(r"^blog/", include("biblion.urls")),

    # url(r"^openid/", include(PinaxConsumer().urls)),

    #temp
    # url(r"^sponsors/", direct_to_template, { "template": "static/sponsors.html", }, name="sponsors"),
    url(r"^venue/", direct_to_template, { "template": "static/venue.html", }, name="venue"),

    url(r"^speaker/", include("symposion.speakers.urls")),
    url(r"^proposals/", include("symposion.proposals.urls")),

    url(r"^sponsors/", include("pycon.sponsorship.urls")),

    url(r"^boxes/", include("symposion.boxes.urls")),
    url(r"^(?P<path>%s)$" % PAGE_RE, "symposion.cms.views.page", name="cms_page"),
)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)