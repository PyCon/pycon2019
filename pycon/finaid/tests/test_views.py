import datetime

from django.contrib.auth.models import User
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from pycon.finaid.models import FinancialAidApplication, \
    FinancialAidApplicationPeriod

from symposion.conference.models import Conference


today = datetime.date.today()
now = datetime.datetime.now()
one_day = datetime.timedelta(days=1)


class TestFinaidApplicationView(TestCase):
    def setUp(self):
        self.edit_url = reverse('finaid_edit')
        self.login_url = reverse('account_login')
        self.dashboard_url = reverse('dashboard')
        self.user = User.objects.create_user('joe',
                                             email='joe@example.com',
                                             password='snoopy')
        # financial aid applications are open
        self.period = FinancialAidApplicationPeriod.objects.create(
            start=today - one_day,
            end=today + one_day
        )
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)

    def login(self):
        # The auth backend that pycon is using is kind of gross. It expects
        # username to contain the email address.
        self.assertTrue(self.client.login(username='joe@example.com',
                                          password='snoopy'),
                        "Login failed")

    def test_not_logged_in(self):
        # If not logged in, view redirects to login
        expected_url = self.login_url + "?next=" + self.edit_url

        rsp = self.client.get(self.edit_url)
        self.assertRedirects(rsp, expected_url)

        rsp = self.client.post(self.edit_url)
        self.assertRedirects(rsp, expected_url)

    def test_logged_in_applications_open(self):
        # If logged in and applications open, we can view the view
        self.login()
        rsp = self.client.get(self.edit_url)
        self.assertEqual(200, rsp.status_code)
        # and context has a form
        form = rsp.context['form']
        # the form is set up to do an application for the current user
        self.assertEqual(self.user, form.instance.user)

    def test_logged_in_applications_closed(self):
        # If logged in and applications closed, we redirect to dashboard
        # We also display a message
        self.login()
        # Applications ended long ago
        self.period.end = datetime.datetime(1972, 1, 1)
        self.period.save()
        rsp = self.client.get(self.edit_url)
        self.assertRedirects(rsp, self.dashboard_url)
        # And a message was displayed
        # Need to tell the test client to follow the redirect if we want
        # to see the message
        rsp = self.client.get(self.edit_url, follow=True)
        context = rsp.context
        self.assertIn('messages', context)
        self.assertEqual(1, len(context['messages']))

    def test_submit(self):
        # Submit an application
        self.login()
        data = dict(
            profession="Foo",
            experience_level="lots",
            what_you_want="money",
            want_to_learn="stuff",
            use_of_python="fun",
            presenting='1',
            hotel_nights='0',
            travel_amount_requested="0.00",
            sex='0',
        )
        self.assertEqual(0, len(mail.outbox))
        rsp = self.client.post(self.edit_url, data)
        self.assertRedirects(rsp, self.dashboard_url)

        # There's an application for this user now
        app = FinancialAidApplication.objects.get(user=self.user)
        self.assertEqual("Foo", app.profession)

        # And an email was sent
        self.assertEqual(1, len(mail.outbox))
        msg = mail.outbox[0]
        # print("From: %s\nTo: %s\nSubject: %s\n\n%s" %
        #       (msg.from_email, ", ".join(msg.recipients()),
        #        msg.subject, msg.body))
        self.assertTrue("received" in msg.body)

        # And a message was displayed
        # Need to tell the test client to follow the redirect if we want
        # to see the message
        rsp = self.client.post(self.edit_url, data, follow=True)
        context = rsp.context
        self.assertIn('messages', context)
        self.assertEqual(1, len(context['messages']))

    def test_edit(self):
        # Edit an application
        self.login()

        # Existing application
        FinancialAidApplication.objects.create(
            user=self.user,
            profession="Foo",
            experience_level="lots",
            what_you_want="money",
            want_to_learn="stuff",
            use_of_python="fun",
            presenting=1,
        )

        # New data
        data = dict(
            profession="Gourmet",
            experience_level="none",
            what_you_want="money",
            want_to_learn="stuff",
            use_of_python="fun",
            presenting='1',
            hotel_nights='0',
            travel_amount_requested="0.00",
            sex='0',
        )

        self.assertEqual(0, len(mail.outbox))
        rsp = self.client.post(self.edit_url, data)
        self.assertRedirects(rsp, self.dashboard_url)
        # And the application now has new data
        app = FinancialAidApplication.objects.get(user=self.user)
        self.assertEqual("Gourmet", app.profession)
        self.assertEqual("none", app.experience_level)
        # And an email was sent
        self.assertEqual(1, len(mail.outbox))
        msg = mail.outbox[0]
        self.assertTrue("edited" in msg.body)
        # And a message was displayed
        # Need to tell the test client to follow the redirect if we want
        # to see the message
        rsp = self.client.post(self.edit_url, data, follow=True)
        context = rsp.context
        self.assertIn('messages', context)
        self.assertEqual(1, len(context['messages']))
