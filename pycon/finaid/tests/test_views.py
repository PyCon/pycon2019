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
    STATUS_INFO_NEEDED, STATUS_OFFERED, STATUS_ACCEPTED, STATUS_DECLINED, STATUS_WITHDRAWN, \
    STATUS_NEED_MORE, PYTHON_EXPERIENCE_EXPERT, PYTHON_EXPERIENCE_BEGINNER
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
            experience_level=PYTHON_EXPERIENCE_EXPERT,
            what_you_want="money",
            use_of_python="fun",
            presenting='1',
            amount_requested="0.00",
            travel_plans="get there",
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
        self.assertEqual(settings.FINANCIAL_AID_EMAIL, msg.from_email)
        self.assertIn("received", msg.body)
        msg = mail.outbox[1]
        self.assertIn(settings.FINANCIAL_AID_EMAIL, msg.recipients())
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
            experience_level=PYTHON_EXPERIENCE_EXPERT,
            what_you_want="money",
            use_of_python="fun",
            presenting=1,
            travel_plans="get there",
        )

        # New data
        data = dict(
            profession="Gourmet",
            experience_level=PYTHON_EXPERIENCE_BEGINNER,
            what_you_want="money",
            use_of_python="fun",
            presenting='1',
            amount_requested="0.00",
            travel_plans="get there quickly",
        )

        self.assertEqual(0, len(mail.outbox))
        rsp = self.client.post(self.edit_url, data)
        self.assertRedirects(rsp, self.dashboard_url)
        # And the application now has new data
        app = FinancialAidApplication.objects.get(user=self.user)
        self.assertEqual("Gourmet", app.profession)
        self.assertEqual(PYTHON_EXPERIENCE_BEGINNER, app.experience_level)
        # And an email was sent to user and committee
        self.assertEqual(2, len(mail.outbox))
        msg = mail.outbox[0]
        self.assertIn("edited", msg.body)
        self.assertIn(settings.FINANCIAL_AID_EMAIL, msg.from_email)
        self.assertIn(app.user.email, msg.recipients())
        self.assertIn(app.fa_app_url(), msg.body)
        msg = mail.outbox[1]
        self.assertIn("edited", msg.body)
        self.assertIn(settings.FINANCIAL_AID_EMAIL, msg.recipients())
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
        self.assertContains(rsp, "Star Trek!")
        self.assertNotContains(rsp, "Burma Shave!")


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
            'amount': Decimal('0.00'),
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
        expected_msgs = [(subject, template_text, settings.FINANCIAL_AID_EMAIL,
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
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)

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


class TestCSVExport(TestMixin, ReviewTestMixin, TestCase):
    def setUp(self):
        super(TestCSVExport, self).setUp()
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

    def test_reviewers_only(self):
        # Only reviewers can download the data
        self.make_not_reviewer(self.user)
        self.login()
        rsp = self.client.get(self.url)
        self.assertEqual(403, rsp.status_code)
        # and non-reviewers don't see the download link on their dashboard
        rsp = self.client.get(reverse('dashboard'))
        self.assertEqual(200, rsp.status_code)
        self.assertNotContains(rsp, self.url)

    def test_link_on_dashboard(self):
        # Reviewers get a link on their dashboard
        self.login()
        rsp = self.client.get(reverse('dashboard'))
        self.assertEqual(200, rsp.status_code)
        self.assertContains(rsp, self.url, msg_prefix=rsp.content.decode('utf-8'))

    def test_empty_data(self):
        # No data, should be able to get a CSV response anyway
        self.login()
        result = self.get_csv()
        self.assertEqual(0, len(result))

    def test_one_application(self):
        # One application that has review data
        # Include non-ASCII to be sure that doesn't break anything
        application = FinancialAidApplication.objects.create(
            user=self.user,
            profession=u"Föo",
            experience_level=PYTHON_EXPERIENCE_BEGINNER,
            what_you_want=u"money\nand\n'lóts' of it.",
            use_of_python="fun",
            presenting=1,
        )
        FinancialAidReviewData.objects.create(
            application=application,
            status=STATUS_INFO_NEEDED,
            amount=Decimal('2.45'),
        )
        self.login()
        result = self.get_csv()
        self.assertEqual(1, len(result))
        app = result[0]
        self.assertEqual(unicode(application.user), app['user'])
        self.assertEqual(application.experience_level, app['experience_level'])
        self.assertEqual("Yes", app['presenting'])
        self.assertEqual("Information needed", app['status'])
        self.assertEqual(self.user.email, app['email'])

    def test_two_applications(self):
        # A couple users and applications, without review data
        user1 = self.create_user("bob", "bob@example.com", "snoopy")
        user2 = self.create_user("fred", "fred@example.com", "linus")

        application1 = create_application(user1,
                                          experience_level=PYTHON_EXPERIENCE_BEGINNER)
        application1.save()
        application2 = create_application(user2)
        application2.save()

        self.login()
        result = self.get_csv()
        self.assertEqual(2, len(result))
        app = result[0]
        self.assertEqual(unicode(application1.user), app['user'])
        self.assertEqual(application1.experience_level, app['experience_level'])
        self.assertEqual('Submitted', app['status'])
        self.assertEqual(user1.email, app['email'])


class TestFinaidDashboardButtons(TestCase, TestMixin):
    def setUp(self):
        super(TestFinaidDashboardButtons, self).setUp()
        self.dashboard_url = reverse('dashboard')
        self.login_url = reverse('account_login')
        self.user = self.create_user()
        self.login()
        # financial aid applications are open
        self.period = FinancialAidApplicationPeriod.objects.create(
            start=today - one_day,
            end=today + one_day
        )
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)

    def assert_buttons(self, button_list):
        """
        Assert that the buttons named in the list are displayed, and
        any not named are not.
        Button names are the corresponding URL name, e.g. 'finaid_edit'
        or 'finaid_withdraw'.
        """
        rsp = self.client.get(self.dashboard_url)
        self.assertEqual(200, rsp.status_code)
        all_buttons = [
            'finaid_apply', 'finaid_withdraw',
            'finaid_decline', 'finaid_accept', 'finaid_request_more',
            'finaid_edit', 'finaid_status', 'finaid_review',
            'finaid_download_csv', 'finaid_provide_info'
        ]
        buttons_in_page = set()
        for name in all_buttons:
            text_repr, real_count, msg_prefix = self._assert_contains(
                rsp, reverse(name), 200, '', False)
            if real_count:
                buttons_in_page.add(name)
        self.assertEqual(set(button_list), buttons_in_page,
                         msg="Expected %r on page, but found %r." % (button_list, buttons_in_page))

    def test_applications_not_open_no_application(self):
        self.period.delete()
        self.assert_buttons([])

    def test_applications_not_open_with_application(self):
        self.period.delete()
        create_application(user=self.user, save=True)
        self.assert_buttons(['finaid_edit', 'finaid_status', 'finaid_withdraw'])

    def test_not_applied(self):
        self.assert_buttons(['finaid_apply'])

    def test_just_submitted(self):
        create_application(user=self.user, save=True)
        self.assert_buttons(['finaid_edit', 'finaid_status', 'finaid_withdraw'])

    def test_offered(self):
        application = create_application(user=self.user, save=True)
        application.set_status(STATUS_OFFERED, save=True)
        self.assert_buttons(['finaid_accept', 'finaid_decline', 'finaid_request_more',
                             'finaid_status'])

    def test_accepted(self):
        application = create_application(user=self.user, save=True)
        application.set_status(STATUS_ACCEPTED, save=True)
        self.assert_buttons(['finaid_status'])

    def test_declined(self):
        application = create_application(user=self.user, save=True)
        application.set_status(STATUS_DECLINED, save=True)
        self.assert_buttons(['finaid_status'])

    def test_withdrawn(self):
        application = create_application(user=self.user, save=True)
        application.set_status(STATUS_WITHDRAWN, save=True)
        self.assert_buttons(['finaid_apply'])

    def test_info_needed(self):
        application = create_application(user=self.user, save=True)
        application.set_status(STATUS_INFO_NEEDED, save=True)
        self.assert_buttons(['finaid_status', 'finaid_provide_info', 'finaid_withdraw'])


class FinaidViewTestMixin(object):
    post_kwargs = {}

    def setUp(self):
        super(FinaidViewTestMixin, self).setUp()
        self.dashboard_url = reverse('dashboard')
        self.login_url = reverse('account_login')
        self.user = self.create_user()
        self.login()
        # financial aid applications are open
        self.period = FinancialAidApplicationPeriod.objects.create(
            start=today - one_day,
            end=today + one_day
        )
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)
        self.url = reverse(self.url_name)
        application = create_application(user=self.user, save=True)
        application.set_status(self.initial_status, save=True)

    def test_get_page(self):
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        application = FinancialAidApplication.objects.get(user=self.user)
        self.assertEqual(self.initial_status, application.status)

    def test_submit(self):
        rsp = self.client.post(self.url, self.post_kwargs)
        self.assertRedirects(rsp, reverse('dashboard'))
        application = FinancialAidApplication.objects.get(user=self.user)
        self.assertEqual(self.final_status, application.status)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, self.subject)


class TestFinaidAccept(FinaidViewTestMixin, TestMixin, TestCase):
    url_name = 'finaid_accept'
    initial_status = STATUS_OFFERED
    final_status = STATUS_ACCEPTED
    subject = 'Joe Smith has accepted their financial aid offer'


class TestFinaidDecline(FinaidViewTestMixin, TestMixin, TestCase):
    url_name = 'finaid_decline'
    initial_status = STATUS_OFFERED
    final_status = STATUS_DECLINED
    subject = 'Joe Smith has declined their financial aid offer'


class TestFinaidWithdraw(FinaidViewTestMixin, TestMixin, TestCase):
    url_name = 'finaid_withdraw'
    initial_status = STATUS_SUBMITTED
    final_status = STATUS_WITHDRAWN
    subject = 'Joe Smith has withdrawn their financial aid application'


class TestFinaidWithdrawWhenInfoNeeded(FinaidViewTestMixin, TestMixin, TestCase):
    url_name = 'finaid_withdraw'
    initial_status = STATUS_INFO_NEEDED
    final_status = STATUS_WITHDRAWN
    subject = 'Joe Smith has withdrawn their financial aid application'


class TestProvideInfoNeeded(FinaidViewTestMixin, TestMixin, TestCase):
    url_name = 'finaid_provide_info'
    initial_status = STATUS_INFO_NEEDED
    final_status = STATUS_SUBMITTED
    post_kwargs = {'message': 'Here you go'}
    subject = 'Message from Joe Smith providing requested information.'


class TestRequestMore(FinaidViewTestMixin, TestMixin, TestCase):
    url_name = 'finaid_request_more'
    initial_status = STATUS_OFFERED
    final_status = STATUS_NEED_MORE
    post_kwargs = {'message': 'I am greed'}
    subject = 'Message from Joe Smith requesting more assistance.'
