import hashlib

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from constance import config

from djangosecure.decorators import frame_deny_exempt


@login_required
def cte_registration_start(request):
    return render(request, "registration/register.html")


@login_required
@frame_deny_exempt
def cte_registration_login(request):
    salt = config.CTE_SECRET
    token = hashlib.sha1(str(request.user.pk) + salt).hexdigest()
    return render(request, "registration/login.html", {
        "token": token,
    })


class GroupRegistration(TemplateView):
    """
    Historically, PyCon occasionally accepts group registrations via a
    spreadsheet. An individual at our registration vendor, CTE, manually
    enters the information provided to create registrations for individual
    attendees.

    CTE registrations are associated with PyCon users via a `pycon_id` (i.e.,
    the primary key of the user). This view allows a CTE registrar to
    bulk-create accounts (or find existing accounts) for individuals and
    retrieve their pycon_id values, so that individuals can log onto PyCon
    later to update their registration information (t-shirt size, etc).

    If an individual does not have a PyCon user account associated with their
    email address, one is created with an unusable password and a password
    reset message is sent to their email address.

    """
    http_method_names = ('get', 'post')
    template_name = "registration/group_registration.html"

    @method_decorator(permission_required("auth.group_registration"))
    def dispatch(self, request, *args, **kwargs):
        return super(GroupRegistration, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass  # TODO
