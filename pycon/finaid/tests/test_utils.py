"""Test for the finaid.utils package"""

import datetime

from mock import patch

from django.core import mail
from django.contrib.auth.models import User, AnonymousUser
from django.template import Template
from django.test import TestCase

from ..models import FinancialAidApplication, FinancialAidApplicationPeriod, \
    PYTHON_EXPERIENCE_BEGINNER
from ..utils import applications_open, has_application, send_email_message


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
            experience_level=PYTHON_EXPERIENCE_BEGINNER,
            what_you_want="money",
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


@patch('pycon.finaid.utils.get_template')
class TestSendEmailMessage(TestCase):
    # def send_email_message(template_name, from_, to, context, header=None):

    def test_send_email_message(self, get_template):
        # send_email_message comes up with the expected template names
        # and creates the EmailMessage with the expected arguments
        test_template = Template("test template")
        get_template.return_value = test_template

        context = {'a': 1, 'b': 2}
        headers = {'Reply-To': 'foo@bar.com'}
        to = ['joe@blow.com', 'jane@doe.com']
        from_ = "from@site.com"
        send_email_message("TESTNAME", from_, to, context, headers)

        args, kwargs = get_template.call_args_list[0]
        expected_template_name = "finaid/email/TESTNAME/subject.txt"
        self.assertEqual(expected_template_name, args[0])

        args, kwargs = get_template.call_args_list[1]
        expected_template_name = "finaid/email/TESTNAME/body.txt"
        self.assertEqual(expected_template_name, args[0])

        self.assertEqual(1, len(mail.outbox))
        msg = mail.outbox[0]
        self.assertEqual(msg.extra_headers, headers)
        self.assertEqual(msg.recipients(), to)
        self.assertEqual(msg.from_email, from_)
