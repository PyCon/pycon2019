from django.conf.urls.defaults import *


urlpatterns = patterns("pycon.profile.views",
    url(r"^edit/$", "profile_edit", name="profile_edit"),
)
