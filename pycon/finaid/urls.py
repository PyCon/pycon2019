from django.conf.urls import patterns, url

from .views import finaid_edit, finaid_review, finaid_status


urlpatterns = patterns("",
    url(r"^edit/$", finaid_edit, name="finaid_edit"),
    url(r"^review/$", finaid_review, name="finaid_review"),
    url(r"^status/$", finaid_status, name="finaid_status"),
)
