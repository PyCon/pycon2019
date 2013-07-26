"""Utilities to help test financial aid"""
from django.contrib.auth.models import User

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


class TestMixin(object):
    def create_user(self, username="joe",
                    email="joe@example.com",
                    password="snoopy"):
        return User.objects.create_user(username,
                                        email=email,
                                        password=password)

    def login(self, username="joe@example.com", password="snoopy"):
        # The auth backend that pycon is using is kind of gross. It expects
        # username to contain the email address.
        self.assertTrue(self.client.login(username=username,
                                          password=password),
                        "Login failed")
