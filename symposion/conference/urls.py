from django.conf.urls import *


urlpatterns = patterns("symposion.conference.views",
    url(r"^users/$", "user_list", name="user_list"),
)
