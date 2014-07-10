from django.conf.urls import url, patterns

from .views import tutorial_email, tutorial_message

urlpatterns = patterns("", # flake8: noqa
    url(r"^mail/(?P<pk>\d+)/(?P<pks>[0-9,]+)/$", tutorial_email, name="tutorial_email"),
    url(r"^message/(?P<pk>\d+)/$", tutorial_message, name="tutorial_message"),
)
