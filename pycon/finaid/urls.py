from django.conf.urls import patterns, url

from .views import finaid_edit, finaid_email, finaid_message, finaid_review, \
    finaid_review_detail, finaid_status, finaid_download_csv


urlpatterns = patterns("",  # noqa
    url(r"^edit/$", finaid_edit, name="finaid_edit"),
    url(r"^review/$", finaid_review, name="finaid_review"),
    url(r"^review/details/(?P<pk>\d+)/$", finaid_review_detail,
        name="finaid_review_detail"),
    url(r"^status/$", finaid_status, name="finaid_status"),
    url(r"^mail/(?P<pks>[0-9,]+)/$", finaid_email, name="finaid_email"),
    url(r"^message/(?P<pks>[0-9,]+)/$", finaid_message, name="finaid_message"),
    url(r"^download/$", finaid_download_csv, name="finaid_download_csv"),
)
