from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

from pycon.finaid.models import FinancialAidApplication
from pycon.finaid.utils import is_reviewer
from symposion.teams.models import Team, Membership

from .utils import TestMixin

class TestFinaidApplicationReview(TestCase, TestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.login_url = reverse('account_login')
        self.review_url = reverse('finaid_review')
        self.team = Team.objects.create(slug="financial-aid-review-team",
                                        name="Finaid review team")
        ct = ContentType.objects.get_for_model(FinancialAidApplication)
        perm = Permission.objects.create(
            codename="review_financial_aid",
            name="Can review financial aid applications",
            content_type=ct)
        self.team.permissions.add(perm)

    def test_not_reviewer(self):
        # Non-reviewers cannot access the review view
        self.login()
        rsp = self.client.get(self.review_url)
        self.assertEqual(403, rsp.status_code)

    def test_reviewer(self):
        # reviewers can access the review view
        Membership.objects.create(team=self.team,
                                  user=self.user,
                                  state="member")
        self.login()
        # The view is not implemented yet, but we won't see the exception
        # until we've passed the access check, so this is a valid test.
        # We'll have to change it when we implement the view, of course.
        with self.assertRaises(NotImplementedError):
            self.client.get(self.review_url)

    def test_non_reviewer_is_reviewer(self):
        self.assertFalse(is_reviewer(self.user))

    def test_reviewer_is_reviewer(self):
        Membership.objects.create(team=self.team,
                                  user=self.user,
                                  state="member")
        self.assertTrue(is_reviewer(self.user))
