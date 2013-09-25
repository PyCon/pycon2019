from django.conf.urls.defaults import url, patterns

from .views import tutorial_email, tutorial_message

urlpatterns = patterns("", # noqa
    url(r"^mail/(?P<pks>[0-9,]+)/$", tutorial_email, name="tutorial_email"),
    url(r"^message/(?P<pk>\d+)/$", tutorial_message, name="tutorial_message"),
)
