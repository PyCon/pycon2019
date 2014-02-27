from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns("pycon.sponsorship.views",  # noqa
    url(r"^$", TemplateView.as_view(template_name="sponsorship/list.html"), name="sponsor_list"),
    url(r"^jobs/$", TemplateView.as_view(template_name="sponsorship/jobs.html"), name="sponsor_jobs"),
    url(r"^apply/$", "sponsor_apply", name="sponsor_apply"),
    url(r"^(?P<pk>\d+)/$", "sponsor_detail", name="sponsor_detail"),
    url(r"^ziplogos/$", "sponsor_zip_logo_files", name="sponsor_zip_logos"),
    url(r"^email/(?P<pks>[\d,]+)/$", "sponsor_email", name="sponsor_email"),
)
