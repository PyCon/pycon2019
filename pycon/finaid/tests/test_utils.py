"""Test for the finaid.utils package"""

import datetime
import unittest

from mock import patch

from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.template import Template
from django.test import TestCase

from ..models import FinancialAidApplication, FinancialAidApplicationPeriod
from ..utils import DEFAULT_EMAIL_ADDRESS, applications_open, \
    email_address, has_application, send_email_message


today = datetime.date.today()


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
        # No FinancialAidApplicationPeriod records - apps closed
        self.assertFalse(applications_open())

    def test_applications_open_start_date_future(self):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=3)
        more_future = future + datetime.timedelta(days=3)
        FinancialAidApplicationPeriod.objects.create(
            start=future,
            end=more_future
        )
        self.assertFalse(applications_open())

    def test_applications_open_end_date_future(self):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=3)
        FinancialAidApplicationPeriod.objects.create(
            start=now,
            end=future
        )
        self.assertTrue(applications_open())

    def test_applications_open_end_date_past(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(days=3)
        more_past = past - datetime.timedelta(days=3)
        FinancialAidApplicationPeriod.objects.create(
            start=more_past,
            end=past
        )
        self.assertFalse(applications_open())

    def test_applications_open_period_future(self):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=3)
        FinancialAidApplicationPeriod.objects.create(
            start=future,
            end=future
        )
        self.assertFalse(applications_open())

    def test_applications_open_period_past(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(days=3)
        FinancialAidApplicationPeriod.objects.create(
            start=past,
            end=past
        )
        self.assertFalse(applications_open())

    def test_applications_open_period_active(self):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(days=3)
        future = now + datetime.timedelta(days=3)
        FinancialAidApplicationPeriod.objects.create(
            start=past,
            end=future
        )
        self.assertTrue(applications_open())

    def test_is_reviewer(self):
        # FIXME - write me once is_reviewer is implemented
        pass

    def test_email_address_default(self):
        # If not set, email address is the default.
        # Set dummy FINANCIAL_AID just so we can delete the setting, and
        # be sure it'll be restored to its pre-test value when we're
        # done.
        expected = DEFAULT_EMAIL_ADDRESS
        with self.settings(FINANCIAL_AID=None):
            # no settings at all
            delattr(settings, 'FINANCIAL_AID')
            self.assertEqual(expected, email_address())
            # email entry not set
            settings.FINANCIAL_AID = {}
            self.assertEqual(expected, email_address())

    def test_email_address_override(self):
        # settings can override email address
        expected = "foo@example.com"
        with self.settings(FINANCIAL_AID={'email': expected}):
            self.assertEqual(expected, email_address())


class TestSendEmailMessage(unittest.TestCase):
    # def send_email_message(template_name, from_, to, context):
    # send_mail(subject, body, from_, to)

    @patch('pycon.finaid.utils.send_mail')
    @patch('pycon.finaid.utils.get_template')
    def test_send_email_message(self, get_template, send_mail):
        # send_email_message comes up with the expected template names
        # and calls send_mail with the expected arguments
        test_template = Template("test template")
        get_template.return_value = test_template

        context = {'a': 1, 'b': 2}
        send_email_message("TESTNAME", "from_address", [1, 2], context)

        args, kwargs = get_template.call_args_list[0]
        expected_template_name = "finaid/email/TESTNAME_subject.txt"
        self.assertEqual(expected_template_name, args[0])

        args, kwargs = get_template.call_args_list[1]
        expected_template_name = "finaid/email/TESTNAME_body.txt"
        self.assertEqual(expected_template_name, args[0])

        send_mail.assert_called_with("test template",
                                     "test template",
                                     "from_address",
                                     [1, 2])
