from django.conf.urls.defaults import url, patterns
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("registration.views",
    url(r"^$", direct_to_template, {"template": "registration/register.html"}, name="registration"),
    url(r"^login/$", "cte_login", name="registration_login"),
)
