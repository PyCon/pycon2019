from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer

#from pycon_project.views import creole_preview


handler500 = "pinax.views.server_error"



urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),

    url(r"^account/signup/$", "pinax.apps.account.views.signup", name="acct_signup"),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/(.*)", PinaxConsumer()),
    url(r"^oauth_access/finish_signup/(?P<service>\w+)/$", "oauth_callbacks.finish_signup", name="oauth_access_finish_signup"),
    url(r"^oauth_access/", include("oauth_access.urls")),
    url(r"^waitinglist/", include("pinax.apps.waitinglist.urls")),
    url(r"^admin/", include(admin.site.urls)),
    
   # url(r"^creole_preview/$", creole_preview, name="creole_preview"),
    
    url(r"^feed/(?P<section>\w+)/$", "biblion.views.blog_feed", name="blog_feed"),
    url(r"^", include("wakawaka.urls")),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        (r"", include("staticfiles.urls")),
    )
