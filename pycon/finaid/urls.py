from django.conf.urls import patterns, url

from .views import finaid_edit, finaid_email, finaid_review, \
    finaid_review_detail, finaid_status


urlpatterns = patterns("",
    url(r"^edit/$", finaid_edit, name="finaid_edit"),
    url(r"^review/$", finaid_review, name="finaid_review"),
    url(r"^review/details/(?P<pk>\d+)/$", finaid_review_detail,
        name="finaid_review_detail"),
    url(r"^status/$", finaid_status, name="finaid_status"),
    url(r"^mail/(?P<pks>[0-9,]+)/$", finaid_email, name="finaid_email"),
)
