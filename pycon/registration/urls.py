from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^register/$",
        views.cte_registration_introduction,
        name="registration_introduction"),
    url(r"^register/form/$",
        views.cte_registration_start,
        name="registration_start"),
    url(r"^register/login/$",
        views.cte_registration_login,
        name="registration_login"),
    url(r"^register/group/$",
        views.GroupRegistration.as_view(),
        name="group_registration"),
]
