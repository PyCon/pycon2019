import datetime

from django.conf import settings
from pycon.finaid.models import FinancialAidApplication


def applications_open():
    """Return True if applications are allowed to be submitted
     and edited at the current time.

    Based on settings.FINANCIAL_AID{'start_date'} and {'end_date'}:


    start_date
        (datetime object) If set, financial aid applications will not be
        accepted or allowed to be edited before this date.
    end_date
        (datetime object) If set, financial aid applications will not be
        accepted or allowed to be edited after this date

    If neither is set, applications are CLOSED.
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
            _ = user.financial_aid
        except (FinancialAidApplication.DoesNotExist, AttributeError):
            user._has_finaid_application = False
        else:
            user._has_finaid_application = True
    return user._has_finaid_application
