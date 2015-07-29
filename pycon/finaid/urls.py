from django.conf.urls import patterns, url

from .views import finaid_edit, finaid_email, finaid_message, finaid_review, \
    finaid_review_detail, finaid_status, finaid_download_csv, finaid_withdraw, \
    finaid_decline, finaid_accept, finaid_request_more, finaid_provide_info


urlpatterns = [
    url(r"^apply/$", finaid_edit, name="finaid_apply"),
    url(r"^edit/$", finaid_edit, name="finaid_edit"),
    url(r'^provide_info/$', finaid_provide_info, name="finaid_provide_info"),
    url(r"^withdraw/$", finaid_withdraw, name="finaid_withdraw"),
    url(r"^decline/$", finaid_decline, name="finaid_decline"),
    url(r"^accept/$", finaid_accept, name="finaid_accept"),
    url(r"^request_more/$", finaid_request_more, name="finaid_request_more"),
    url(r"^review/$", finaid_review, name="finaid_review"),
    url(r"^review/(?P<pks>[0-9,]+)/$", finaid_review, name="finaid_review"),
    url(r"^review/details/(?P<pk>\d+)/$", finaid_review_detail,
        name="finaid_review_detail"),
    url(r"^status/$", finaid_status, name="finaid_status"),
    url(r"^mail/(?P<pks>[0-9,]+)/$", finaid_email, name="finaid_email"),
    url(r"^message/(?P<pks>[0-9,]+)/$", finaid_message, name="finaid_message"),
    url(r"^download/$", finaid_download_csv, name="finaid_download_csv"),
]
