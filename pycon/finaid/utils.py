import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from pycon.finaid.models import FinancialAidApplication

DEFAULT_EMAIL_ADDRESS = "pycon-aid@pycon.org"


def applications_open():
    """Return True if applications are allowed to be submitted
     and edited at the current time.

    Based on settings.FINANCIAL_AID['start_date'] and ['end_date']:


    start_date
        (datetime object) If set, financial aid applications will not be
        accepted or allowed to be edited before this date.
    end_date
        (datetime object) If set, financial aid applications will not be
        accepted or allowed to be edited after this date

    If neither is set, applications are closed.
    """
    now = datetime.datetime.now()
    if hasattr(settings, "FINANCIAL_AID"):
        finaid_settings = settings.FINANCIAL_AID
    else:
        finaid_settings = {}
    start_date = finaid_settings.get('start_date', None)
    end_date = finaid_settings.get('end_date', None)
    if not start_date and not end_date:
        return False
    if start_date and now < start_date:
        return False
    if end_date and end_date < now:
        return False
    return True


def is_reviewer(user):
    """Return True if this user is a financial aid reviewer"""
    # FIXME - not implemented yet
    # Cache on user object when we do implement it, since we call
    # this repeatedly on the same user
    return False


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


def email_address():
    """
    Return the email address that financial aid emails should come from,
    applications should send emails to with questions, etc.

    Default is ``pycon-aid@pycon.org``. Override by setting
    FINANCIAL_AID['email'].
    """
    return getattr(settings, "FINANCIAL_AID", {})\
        .get('email', DEFAULT_EMAIL_ADDRESS)


def send_email_message(template_name, from_, to, context):
    """
    Send an email message.

    :param template_name: Use to construct the real template names for the
    subject and body like this: "finaid/email/%(template_name)s_subject.txt"
    and "finaid/email/%(template_name)s_body.txt"
    :param from_: From address to use
    :param to: List of addresses to send to
    :param context: Dictionary with context to use when rendering the
    templates.
    """
    context = Context(context)

    name = "finaid/email/%s_subject.txt" % template_name
    subject_template = get_template(name)
    subject = subject_template.render(context)
    # subjects must be a single line, no newlines
    # if there's a trailing newline, strip it; anything more than that,
    # let it fail (tests will fail) so we know the subject template is
    # not valid.
    subject = subject.rstrip(u"\n")

    name = "finaid/email/%s_body.txt" % template_name
    body_template = get_template(name)
    body = body_template.render(context)

    # Important: By default, the MIME type of the body parameter in an
    # EmailMessage is "text/plain". That makes it safe to use "|safe" in
    # our email templates, and we do. If you change this to, say, send
    # HTML format email, you must go through the email templates and do
    # something better about escaping user data for safety.

    send_mail(subject, body, from_, to)
