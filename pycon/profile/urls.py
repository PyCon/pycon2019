from django.conf.urls import *


urlpatterns = patterns("pycon.profile.views",
    url(r"^edit/$", "profile_edit", name="profile_edit"),
)
