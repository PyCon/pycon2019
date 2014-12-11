import hashlib
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from constance import config

from djangosecure.decorators import frame_deny_exempt

from .forms import GroupRegistrationForm


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
    spreadsheet. An employee at our registration vendor, CTE, manually
    enters the spreadsheet data to create registrations for individual
    attendees.

    CTE registrations are associated with PyCon users via a `pycon_id` (i.e.,
    the primary key of the user). This view allows a CTE registrar to
    bulk-create accounts (or find existing accounts) for individuals and
    retrieve their pycon_id values, so that individuals can log onto PyCon
    later to update their registration information (t-shirt size, etc).

    If an individual does not have a PyCon user account associated with their
    email address, one is created with an unusable password and a password
    reset message is sent to their email address.

    This view is atomic - users are only created if all registration data
    is valid.

    """
    format_error = ("Group registration data must be a JSON-encoded list of "
                    "registration data dictionaries.")
    http_method_names = ('get', 'post')
    template_name = "registration/group_registration.html"

    @method_decorator(permission_required("auth.group_registration"))
    def dispatch(self, request, *args, **kwargs):
        return super(GroupRegistration, self).dispatch(request, *args, **kwargs)

    @transaction.commit_manually
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except:
            return HttpResponseBadRequest(self.format_error)

        # Data should be a list of registration info in dictionary format.
        if not (isinstance(data, list) and all([isinstance(d, dict) for d in data])):
            return HttpResponseBadRequest(self.format_error)

        all_valid = True
        seen_emails = []
        user_data = []
        for registration in data:
            form = GroupRegistrationForm(data=registration)
            if form.is_valid():
                # Check if this is a duplicate of an email provided in this request.
                email = User.objects.normalize_email(form.cleaned_data['email'])
                if email in seen_emails:
                    all_valid = False
                    user_data.append({
                        'valid': False,
                        'error_message': 'This email is a duplicate of one above.',
                        'user': None,
                    })
                else:
                    seen_emails.append(email)
                    created, user = form.save()
                    user_data.append({
                        'valid': True,
                        'created': created,
                        'user': {
                            'pycon_id': user.pk,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                        }
                    })
            else:
                all_valid = False
                user_data.append({
                    'valid': False,
                    'error_message': 'An error occurred.',  # TODO
                    'user': None,
                })

        # The request is atomic - all users are created (or found), or none
        # are.
        if not all_valid:
            for d in user_data:
                d['user'] = None
                d.pop('created', None)

            transaction.rollback()
        else:
            transaction.commit()
            for d in user_data:
                if d['created']:
                    GroupRegistration.send_password_reset_email(d['user'])

        return_data = {'success': all_valid, 'users': user_data}
        return HttpResponse(json.dumps(return_data))

    @staticmethod
    def send_password_reset_email(user):
        pass
