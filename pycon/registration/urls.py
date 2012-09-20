from django.conf.urls.defaults import url, patterns
from django.views.generic.simple import direct_to_template

from django.contrib.auth.decorators import login_required


urlpatterns = patterns("pycon.registration.views",
    url(r"^register/$", login_required(direct_to_template), {"template": "registration/register.html"}, name="registration_start"),
    url(r"^register/login/$", "cte_login", name="registration_login"),
)
