from django.conf.urls import url

from .views import finaid_edit, finaid_email, finaid_message, finaid_review, \
    finaid_review_detail, finaid_status, finaid_download_csv, \
    phyllis_finaid_download_csv, speaker_grant_edit, \
    receipt_upload, FinaidAcceptView, FinaidDeclineView, \
    FinaidProvideInfoView, FinaidWithdrawView, FinaidRequestMoreView


urlpatterns = [
    url(r"^apply/$", finaid_edit, name="finaid_apply"),
    url(r"^edit/$", finaid_edit, name="finaid_edit"),
    url(r"^speaker/apply/$", speaker_grant_edit, name="speaker_grant_apply"),
    url(r"^speaker/edit/$", speaker_grant_edit, name="speaker_grant_edit"),
    url(r'^provide_info/$', FinaidProvideInfoView.as_view(), name="finaid_provide_info"),
    url(r"^withdraw/$", FinaidWithdrawView.as_view(), name="finaid_withdraw"),
    url(r"^decline/$", FinaidDeclineView.as_view(), name="finaid_decline"),
    url(r"^accept/$", FinaidAcceptView.as_view(), name="finaid_accept"),
    url(r"^request_more/$", FinaidRequestMoreView.as_view(), name="finaid_request_more"),
    url(r"^review/$", finaid_review, name="finaid_review"),
    url(r"^review/(?P<pks>[0-9,]+)/$", finaid_review, name="finaid_review"),
    url(r"^review/details/(?P<pk>\d+)/$", finaid_review_detail,
        name="finaid_review_detail"),
    url(r"^status/$", finaid_status, name="finaid_status"),
    url(r"^mail/(?P<pks>[0-9,]+)/$", finaid_email, name="finaid_email"),
    url(r"^message/(?P<pks>[0-9,]+)/$", finaid_message, name="finaid_message"),
    url(r"^download/$", finaid_download_csv, name="finaid_download_csv"),
    url(r"^phyllis_download/$", phyllis_finaid_download_csv, name="phyllis_finaid_download_csv"),
    url(r"^receipt_upload/$", receipt_upload, name="receipt_upload"),

]
