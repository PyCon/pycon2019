from django.conf.urls import *
  
urlpatterns = patterns("pycon.mentorship.views",
    url(r"^view/$", "mentorship_signup_view_slots", name="mentorship_signup_view"),
)
