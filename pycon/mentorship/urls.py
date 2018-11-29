from django.conf.urls import *
  
urlpatterns = patterns("pycon.mentorship.views",
    url(r"^form/$", "mentorship_view", name="mentorship_view"),
)
