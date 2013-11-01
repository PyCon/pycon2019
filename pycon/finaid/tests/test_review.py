from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from pycon.finaid.models import STATUS_REJECTED, STATUS_SUBMITTED, \
    FinancialAidMessage, FinancialAidReviewData
from pycon.finaid.utils import is_reviewer
from symposion.conference.models import Conference

from .utils import TestMixin, create_application, ReviewTestMixin


class TestFinaidApplicationReview(TestCase, TestMixin, ReviewTestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.login_url = reverse('account_login')
        self.review_url = reverse('finaid_review')
        self.setup_reviewer_team_and_permissions()

    def test_not_reviewer(self):
        # Non-reviewers cannot access the review view
        self.login()
        rsp = self.client.get(self.review_url)
        self.assertEqual(403, rsp.status_code)

    def test_reviewer(self):
        # reviewers can access the review view
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)
        self.make_reviewer(self.user)
        self.login()
        rsp = self.client.get(self.review_url)
        self.assertEqual(200, rsp.status_code)

    def test_non_reviewer_is_reviewer(self):
        self.assertFalse(is_reviewer(self.user))

    def test_reviewer_is_reviewer(self):
        self.make_reviewer(self.user)
        self.assertTrue(is_reviewer(self.user))

    def test_submit_message(self):
        self.make_reviewer(self.user)
        self.login()
        # create application
        applicant = self.create_user(username="jane",
                                     email="jane@example.com")
        application = create_application(user=applicant)
        application.save()
        # form data
        MESSAGE = "now is the time for all good parties to..."
        data = {
            'application': application,
            'user': self.user,
            'visible': False,
            'message': MESSAGE,
            'message_submit': 'message_submit',
        }
        url = reverse('finaid_review_detail', kwargs={'pk': application.pk})
        rsp = self.client.post(url, data, follow=True)
        self.assertEqual(200, rsp.status_code)
        msg = FinancialAidMessage.objects.filter(user=self.user,
                                                 application=application)[0]
        self.assertEqual(MESSAGE, msg.message)

    def test_reviewer_view_messages(self):
        self.make_reviewer(self.user)
        self.login()
        # create application
        applicant = self.create_user(username="jane",
                                     email="jane@example.com")
        application = create_application(user=applicant)
        application.save()
        # create message that is only visible to reviewers
        message = FinancialAidMessage.objects.create(
            application=application,
            user=self.user,
            visible=False
        )

        url = reverse('finaid_review_detail', kwargs={'pk': application.pk})
        rsp = self.client.get(url)
        self.assertEqual(200, rsp.status_code)
        review_messages = rsp.context['review_messages']
        self.assertIn(message, review_messages)

    def test_update_review_data(self):
        self.make_reviewer(self.user)
        self.login()
        # create application
        applicant = self.create_user(username="jane",
                                     email="jane@example.com")
        application = create_application(user=applicant)
        application.save()
        # Create review record
        # Most fields are optional
        data = {
            'application': application,
            'status': STATUS_SUBMITTED,
            'hotel_amount': Decimal('6.66'),
            'registration_amount': Decimal('0.00'),
            'travel_amount': Decimal('0.00'),
        }
        review = FinancialAidReviewData(**data)
        review.save()

        # Now, submit the form to change the status
        data['status'] = STATUS_REJECTED
        data['hotel_amount'] = Decimal('7.77')
        data['review_submit'] = 'review_submit'

        url = reverse('finaid_review_detail', kwargs={'pk': application.pk})
        rsp = self.client.post(url, data, follow=False)
        self.assertEqual(302, rsp.status_code)
        new_review = FinancialAidReviewData.objects.get(pk=review.pk)
        self.assertEqual(STATUS_REJECTED, new_review.status)
        self.assertEqual(Decimal("7.77"), new_review.hotel_amount)


class TestFinaidApplicationReviewDetail(TestCase, TestMixin, ReviewTestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.applicant = self.create_user("fred", "fred@example.com", "linus")
        self.application = create_application(user=self.applicant)
        self.application.save()
        self.review_url = reverse('finaid_review_detail', kwargs={'pk': self.application.pk})
        self.setup_reviewer_team_and_permissions()

    def test_not_reviewer_not_applicant(self):
        # Non-reviewers cannot access the review view
        self.login()
        rsp = self.client.get(self.review_url)
        self.assertEqual(403, rsp.status_code)

    def test_not_reviewer_is_applicant(self):
        # Non-reviewer applicants are redirected to finaid_edit
        self.login(username="fred@example.com", password="linus")
        rsp = self.client.get(self.review_url)
        self.assertEqual(302, rsp.status_code)

    def test_reviewer(self):
        # reviewers can access the review view
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)
        self.login()
        self.make_reviewer(self.user)
        rsp = self.client.get(self.review_url)
        self.assertEqual(200, rsp.status_code)
