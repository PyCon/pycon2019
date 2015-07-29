from django.conf import settings
from django.core.mail.message import EmailMessage
from django.template import Context, Template
from django.template.loader import get_template
from pycon.finaid.models import FinancialAidApplication, \
    FinancialAidApplicationPeriod, STATUS_WITHDRAWN


DEFAULT_EMAIL_ADDRESS = "pycon-aid@python.org"


def applications_open():
    """Return True if applications are allowed to be submitted
     and edited at the current time.

    Based on there being a FinancialAidApplicationPeriod record
    encompassing the current time.
    """
    return FinancialAidApplicationPeriod.open()


def is_reviewer(user):
    """Return True if this user is a financial aid reviewer"""
    # no need to cache here, all the DB lookups used during has_perm
    # are already cached

    return user.has_perm("finaid.review_financial_aid")


def has_application(user):
    """Return True if this user has submitted an application"""
    if not hasattr(user, "_has_finaid_application"):
        try:
            getattr(user, 'financial_aid')
        except (FinancialAidApplication.DoesNotExist, AttributeError):
            user._has_finaid_application = False
        else:
            user._has_finaid_application = True
    return user._has_finaid_application


def has_withdrawn_application(user):
    if not has_application(user):
        return False
    return user.financial_aid.status == STATUS_WITHDRAWN


def email_address():
    """
    Return the email address that financial aid emails should come from,
    applications should send emails to with questions, etc.

    Default is ``pycon-aid@python.org``. Override by setting
    FINANCIAL_AID['email'].
    """
    return getattr(settings, "FINANCIAL_AID", {})\
        .get('email', DEFAULT_EMAIL_ADDRESS)


def email_context(request, application, message=None):
    """
    Return a dictionary with the context to be used when constructing
    email messages about this application from a template.
    """
    fa_app_url = request.build_absolute_uri(application.fa_app_url())
    context = {
        'user': request.user,
        'message': message,
        'application': application,
        'applicant': application.user,
        'fa_app_url': fa_app_url,
    }
    return context


def send_email_message(template_name, from_, to, context, headers=None, subject_template=None):
    """
    Send an email message.

    :param template_name: Use to construct the real template names for the
    subject and body like this: "finaid/email/%(template_name)s/subject.txt"
    and "finaid/email/%(template_name)s/body.txt"
    :param from_: From address to use
    :param to: List of addresses to send to
    :param context: Dictionary with context to use when rendering the
    templates.
    :param headers: dict of optional, additional email headers
    :param subject_template: optional string to use as the subject template, in place of
       finaid/email/{{ template_name }}/subject.txt
    """
    context = Context(context)

    name = "finaid/email/%s/subject.txt" % template_name
    if subject_template:
        subject_template = Template(subject_template)
    else:
        subject_template = get_template(name)
    subject = subject_template.render(context)
    # subjects must be a single line, no newlines
    # if there's a trailing newline, strip it; anything more than that,
    # let it fail (tests will fail) so we know the subject template is
    # not valid.
    subject = subject.rstrip(u"\n")

    name = "finaid/email/%s/body.txt" % template_name
    body_template = get_template(name)
    body = body_template.render(context)

    # Important: By default, the MIME type of the body parameter in an
    # EmailMessage is "text/plain". That makes it safe to use "|safe" in
    # our email templates, and we do. If you change this to, say, send
    # HTML format email, you must go through the email templates and do
    # something better about escaping user data for safety.

    email = EmailMessage(subject, body, from_, to, headers=headers)
    email.send()
