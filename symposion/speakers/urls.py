from django.conf.urls.defaults import *


urlpatterns = patterns("symposion.speakers.views",
    url(r"^create/$", "speaker_create", name="speaker_create"),
    url(r"^edit/(?:(?P<pk>\d+)/)?$", "speaker_edit", name="speaker_edit"),
    url(r"^profile/(?P<pk>\d+)/$", "speaker_profile", name="speaker_profile"),
)
