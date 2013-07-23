import datetime
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase

from ..models import FinancialAidApplication
from ..utils import has_application, applications_open


class TestFinAidUtils(TestCase):
    def test_has_application_anonymous(self):
        user = AnonymousUser()
        self.assertFalse(has_application(user))

    def test_has_application_false(self):
        user = User.objects.create_user('joe')
        self.assertFalse(has_application(user))

    def test_has_application_true(self):
        user = User.objects.create_user('joe')
         # Just the minimum required fields
        FinancialAidApplication.objects.create(
            user=user,
            profession="Foo",
            experience_level="lots",
            what_you_want="money",
            want_to_learn="stuff",
            use_of_python="fun",
            presenting=1,
        )
        self.assertTrue(has_application(user))

    def test_applications_open_no_dates(self):
        # No dates in settings - applications are closed
        # Set dummy FINANCIAL_AID just so we can delete the setting, and
        # be sure it'll be restored to its pre-test value when we're
        # done.
        with self.settings(FINANCIAL_AID=None):
            # no setting
            delattr(settings, 'FINANCIAL_AID')
            self.assertFalse(applications_open())
            # no dates
            settings.FINANCIAL_AID = {}
            self.assertFalse(applications_open())

    def test_applications_open_start_date_future(self):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=3)
        finaid_settings = {
            'start_date': future,
        }
        with self.settings(FINANCIAL_AID=finaid_settings):
            self.assertFalse(applications_open())

    def test_applications_open_start_date_past(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(days=3)
        finaid_settings = {
            'start_date': past,
        }
        with self.settings(FINANCIAL_AID=finaid_settings):
            self.assertTrue(applications_open())

    def test_applications_open_end_date_future(self):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=3)
        finaid_settings = {
            'end_date': future,
        }
        with self.settings(FINANCIAL_AID=finaid_settings):
            self.assertTrue(applications_open())

    def test_applications_open_end_date_past(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(days=3)
        finaid_settings = {
            'end_date': past,
        }
        with self.settings(FINANCIAL_AID=finaid_settings):
            self.assertFalse(applications_open())

    def test_applications_open_period_future(self):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=3)
        finaid_settings = {
            'start_date': future,
            'end_date': future,
        }
        with self.settings(FINANCIAL_AID=finaid_settings):
            self.assertFalse(applications_open())

    def test_applications_open_period_past(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(days=3)
        finaid_settings = {
            'start_date': past,
            'end_date': past,
        }
        with self.settings(FINANCIAL_AID=finaid_settings):
            self.assertFalse(applications_open())

    def test_applications_open_period_active(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(days=3)
        future = now + datetime.timedelta(days=3)
        finaid_settings = {
            'start_date': past,
            'end_date': future,
        }
        with self.settings(FINANCIAL_AID=finaid_settings):
            self.assertTrue(applications_open())

    def test_is_reviewer(self):
        # FIXME - write me once is_reviewer is implemented
        pass
