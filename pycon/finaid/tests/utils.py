"""Utilities to help test financial aid"""
from pycon.finaid.models import FinancialAidApplication


def create_application(user, **kwargs):
    """Return application object (unsaved) for this user."""
    defaults = dict(
        user=user,
        profession="Foo",
        experience_level="lots",
        what_you_want="money",
        want_to_learn="stuff",
        use_of_python="fun",
        presenting=1,
    )
    defaults.update(kwargs)
    return FinancialAidApplication(**defaults)
