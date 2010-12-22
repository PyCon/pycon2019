from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r"^campaign/create/$", "user_mailer.views.campaign_create", name="campaign_create"),
    url(r"^campaign/(\d+)/review/$", "user_mailer.views.campaign_review", name="campaign_review"),
    url(r"^campaign/(\d+)/email_preview/(\d+)/$", "user_mailer.views.campaign_email_preview", name="campaign_email_preview"),
    url(r"^campaign/(\d+)/submit/$", "user_mailer.views.campaign_submit", name="campaign_submit"),
)
