from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

# from pinax.apps.account.openid_consumer import PinaxConsumer


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("symposion.about.urls")),
    url(r"^account/", include("account.urls")),
    # url(r"^openid/", include(PinaxConsumer().urls)),

    #temp
    url(r"^sponsors/", direct_to_template, { "template": "static/sponsors.html", }, name="sponsors"),
    url(r"^venue/", direct_to_template, { "template": "static/venue.html", }, name="venue"),
    url(r"^speaker/", direct_to_template, { "template": "static/speaker_detail.html", }, name="speaker"),
    url(r"^cms/", direct_to_template, { "template": "static/simple.html", }, name="cms"),
)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)