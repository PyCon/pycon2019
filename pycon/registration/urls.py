from django.conf.urls import url, patterns

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = patterns("pycon.registration.views",
    url(r"^register/$", login_required(TemplateView.as_view(template_name="registration/register.html")), name="registration_start"),
    url(r"^register/login/$", "cte_login", name="registration_login"),
)
