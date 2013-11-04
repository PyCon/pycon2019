# coding=utf-8
from cStringIO import StringIO
import csv
import datetime
from decimal import Decimal

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from mock import patch

from pycon.finaid.models import FinancialAidApplication, \
    FinancialAidApplicationPeriod, FinancialAidMessage, \
    FinancialAidEmailTemplate, STATUS_SUBMITTED, FinancialAidReviewData, \
    STATUS_INFO_NEEDED
from pycon.finaid.utils import email_address
from .utils import TestMixin, create_application, ReviewTestMixin

from symposion.conference.models import Conference


today = datetime.date.today()
now = datetime.datetime.now()
one_day = datetime.timedelta(days=1)


class TestFinaidApplicationView(TestCase, TestMixin):
    def setUp(self):
        self.edit_url = reverse('finaid_edit')
        self.dashboard_url = reverse('dashboard')
        self.login_url = reverse('account_login')
        self.user = self.create_user()
        # financial aid applications are open
        self.period = FinancialAidApplicationPeriod.objects.create(
            start=today - one_day,
            end=today + one_day
        )
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)

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

        # And an email was sent to both user and committee
        self.assertEqual(2, len(mail.outbox))
        msg = mail.outbox[0]
        # print("From: %s\nTo: %s\nSubject: %s\n\n%s" %
        #       (msg.from_email, ", ".join(msg.recipients()),
        #        msg.subject, msg.body))
        self.assertIn(app.user.email, msg.recipients())
        self.assertEqual(email_address(), msg.from_email)
        self.assertIn("received", msg.body)
        msg = mail.outbox[1]
        self.assertIn(email_address(), msg.recipients())
        self.assertEqual(app.user.email, msg.from_email)
        self.assertIn("submitted", msg.body)

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
        # And an email was sent to user and committee
        self.assertEqual(2, len(mail.outbox))
        msg = mail.outbox[0]
        self.assertIn("edited", msg.body)
        self.assertIn(email_address(), msg.from_email)
        self.assertIn(app.user.email, msg.recipients())
        self.assertIn(app.fa_app_url(), msg.body)
        msg = mail.outbox[1]
        self.assertIn("edited", msg.body)
        self.assertIn(email_address(), msg.recipients())
        self.assertIn(app.user.email, msg.from_email)
        self.assertIn(app.fa_app_url(), msg.body)
        # And a message was displayed
        # Need to tell the test client to follow the redirect if we want
        # to see the message
        rsp = self.client.post(self.edit_url, data, follow=True)
        context = rsp.context
        self.assertIn('messages', context)
        self.assertEqual(1, len(context['messages']))


class TestFinaidStatusView(TestCase, TestMixin):
    def setUp(self):
        self.edit_url = reverse('finaid_edit')
        self.dashboard_url = reverse('dashboard')
        self.login_url = reverse('account_login')
        self.user = self.create_user()
        # financial aid applications are open
        self.period = FinancialAidApplicationPeriod.objects.create(
            start=today - one_day,
            end=today + one_day
        )
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)

    def test_applicant_cant_see_private_messages(self):
        self.login()
        application = create_application(user=self.user)
        application.save()

        # Create a 2nd user to make a message
        user2 = self.create_user(username="fred", email="fred@example.com")
        # Make message
        FinancialAidMessage.objects.create(user=user2,
                                           application=application,
                                           visible=False,
                                           message="Burma Shave!")
        # Make visible message, just to be sure we're seeing some messages
        FinancialAidMessage.objects.create(user=user2,
                                           application=application,
                                           visible=True,
                                           message="Star Trek!")
        # Status view
        url = reverse("finaid_status")
        rsp = self.client.get(url)
        self.assertIn("Star Trek!", rsp.content)
        self.assertNotIn("Burma Shave!", rsp.content)


class TestFinaidEmailView(TestCase, TestMixin, ReviewTestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.make_reviewer(self.user)
        self.login()
        self.application = create_application(user=self.user)
        self.application.save()
        self.url = reverse('finaid_email', kwargs={'pks': self.application.pk})
        # Create 2nd user and application, just to make sure we're only
        # using the ones that were asked for and not all of them.
        self.user2 = self.create_user(username="jill",
                                      email="jill@example.com")
        self.application2 = create_application(user=self.user2)
        self.application2.save()

    def test_email_view(self):
        # Just look at the email view, check the context
        rsp = self.client.get(self.url)
        if rsp.status_code == 302:
            self.fail(rsp['Location'])
        self.assertEqual(200, rsp.status_code)
        context = rsp.context
        self.assertEqual([self.user], context['users'])

    @patch('django.template.Template.render')
    @patch('pycon.finaid.views.send_mass_mail')
    def test_email_submit(self, mock_send_mass_mail, mock_render):
        # Actually submit the thing

        # Create review record
        # Most fields are optional
        data = {
            'application': self.application,
            'status': STATUS_SUBMITTED,
            'hotel_amount': Decimal('6.66'),
            'registration_amount': Decimal('0.00'),
            'travel_amount': Decimal('0.00'),
        }
        review = FinancialAidReviewData(**data)
        review.save()

        subject = 'TEST SUBJECT'
        template_text = 'THE TEMPLATE'
        FinancialAidEmailTemplate.objects.create(
            name='template',
            template="wrong template"
        )
        template2 = FinancialAidEmailTemplate.objects.create(
            name='template',
            template=template_text,
        )
        data = {
            'template': template2.pk,
            'subject': subject,
        }
        mock_render.return_value = template_text
        rsp = self.client.post(self.url, data)
        self.assertEqual(302, rsp.status_code, rsp.content)
        # we tried to send the right emails
        expected_msgs = [(subject, template_text, email_address(),
                          [self.user.email])]
        mock_send_mass_mail.assert_called_with(expected_msgs)
        # the template was rendered with a good context
        context = mock_render.call_args[0][0]
        self.assertEqual(self.application, context['application'])
        self.assertEqual(review, context['review'])


class TestFinaidMessageView(TestCase, TestMixin, ReviewTestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.make_reviewer(self.user)
        self.login()

    def test_reviewers_only(self):
        self.make_not_reviewer(self.user)
        user1 = self.create_user("bob", "bob@example.com", "snoopy")
        application1 = create_application(user1)
        application1.save()
        url = reverse('finaid_message', kwargs={'pks': str(application1.pk)})

        rsp = self.client.get(url)
        self.assertEqual(403, rsp.status_code)
        rsp = self.client.post(url)
        self.assertEqual(403, rsp.status_code)

    def test_no_applications(self):
        # No applications selected - redirect back to reviewing page
        # (select a non-existing application to get past the URL pattern)
        url = reverse('finaid_message', kwargs={'pks': '999'})
        rsp = self.client.get(url)
        self.assertEqual(302, rsp.status_code)

    def test_messaging(self):
        # Create a couple users and applications
        user1 = self.create_user("bob", "bob@example.com", "snoopy")
        user2 = self.create_user("fred", "fred@example.com", "linus")

        application1 = create_application(user1)
        application1.save()
        application2 = create_application(user2)
        application2.save()

        # We can display the page prompting for a message to send them
        pks = ','.join(str(a.pk) for a in FinancialAidApplication.objects.all())
        url = reverse('finaid_message', kwargs={'pks': pks})
        rsp = self.client.get(url)
        self.assertEqual(200, rsp.status_code)
        context = rsp.context
        applications = context['applications']
        self.assertEqual(2, len(applications))
        self.assertIn(application1, applications)
        self.assertIn(application2, applications)

        # "Send" a message to those two applications
        test_message = 'One if by land and two if by sea'
        data = {
            'visible': 'checked',
            'message': test_message,
        }
        rsp = self.client.post(url, data=data)
        self.assertEqual(302, rsp.status_code)
        msg1 = FinancialAidMessage.objects.get(application=application1)
        self.assertEqual(test_message, msg1.message)
        msg2 = FinancialAidMessage.objects.get(application=application2)
        self.assertEqual(test_message, msg2.message)

        # For each message, it's visible, so it should have been emailed to
        # both the applicant and the reviewers. Total: 4 messages
        self.assertEqual(4, len(mail.outbox))


class TestCSVExport(TestCase, TestMixin, ReviewTestMixin):
    def setUp(self):
        self.url = reverse('finaid_download_csv')
        self.login_url = reverse('account_login')
        self.user = self.create_user()
        self.make_reviewer(self.user)

    def get_csv(self):
        # Call the URL, get the response, parse it strictly as CSV,
        # and return the list of dictionaries
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        dialect = csv.excel()
        dialect.strict = True
        reader = csv.DictReader(StringIO(rsp.content), dialect=dialect)
        result = []
        for item in reader:
            for k, v in item.iteritems():
                item[k] = v.decode('utf-8')
            result.append(item)
        return result

    def test_not_logged_in(self):
        # If not logged in, view redirects to login
        expected_url = self.login_url + "?next=" + self.url

        rsp = self.client.get(self.url)
        self.assertRedirects(rsp, expected_url)

        rsp = self.client.post(self.url)
        self.assertRedirects(rsp, expected_url)

    def test_empty_data(self):
        # No data, should be able to get a CSV response anyway
        self.login()
        result = self.get_csv()
        self.assertEqual(0, len(result))

    def test_one_application(self):
        # One application that has review data
        # Include non-ASCII to be sure that doesn't break anything
        # Make sure the pseudo-field 'sum' is included
        application = FinancialAidApplication.objects.create(
            user=self.user,
            profession=u"Föo",
            experience_level="lots",
            what_you_want=u"money\nand\n'lóts' of it.",
            want_to_learn=u'stuff "and" nončents',
            use_of_python="fun",
            presenting=1,
        )
        FinancialAidReviewData.objects.create(
            application=application,
            status=STATUS_INFO_NEEDED,
            hotel_amount=Decimal('1.23'),
            travel_amount=Decimal('2.45'),
        )
        self.login()
        result = self.get_csv()
        self.assertEqual(1, len(result))
        app = result[0]
        self.assertEqual(unicode(application.user), app['user'])
        self.assertEqual(application.experience_level, app['experience_level'])
        self.assertEqual(application.want_to_learn, app['want_to_learn'])
        self.assertEqual("Yes", app['presenting'])
        self.assertEqual("Information needed", app['status'])
        self.assertEqual("1.23", app['hotel_amount'])
        self.assertEqual("3.68", app['sum'])

    def test_two_applications(self):
        # A couple users and applications, without review data
        user1 = self.create_user("bob", "bob@example.com", "snoopy")
        user2 = self.create_user("fred", "fred@example.com", "linus")

        application1 = create_application(user1,
                                          experience_level="foo\nbar",
                                          sex=2)
        application1.save()
        application2 = create_application(user2, want_to_learn="not really")
        application2.save()

        self.login()
        result = self.get_csv()
        self.assertEqual(2, len(result))
        app = result[0]
        self.assertEqual(unicode(application1.user), app['user'])
        self.assertEqual('Male', app['sex'])
        self.assertEqual(application1.experience_level, app['experience_level'])
        self.assertEqual(application1.want_to_learn, app['want_to_learn'])
        self.assertEqual('Submitted', app['status'])
        self.assertEqual('0.00', app['sum'])
