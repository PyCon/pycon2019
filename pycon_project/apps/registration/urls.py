from django.conf.urls.defaults import url, patterns
from django.views.generic.simple import direct_to_template

from django.contrib.auth.decorators import login_required


urlpatterns = patterns("registration.views",
    url(r"^$", direct_to_template, {"template": "pycon/registration.html"}, name="registration"),
    url(r"^register/$", login_required(direct_to_template), {"template": "registration/register.html"}, name="registration_start"),
    url(r"^login/$", "cte_login", name="registration_login"),
)
