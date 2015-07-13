"""Utilities to help test financial aid"""
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from pycon.finaid.models import FinancialAidApplication
from symposion.conference.models import Conference
from symposion.teams.models import Team, Membership


def create_application(user, **kwargs):
    """Return application object (unsaved) for this user."""
    defaults = dict(
        user=user,
        profession="Foo",
        experience_level="lots",
        what_you_want="money",
        use_of_python="fun",
        presenting=1,
    )
    defaults.update(kwargs)
    return FinancialAidApplication(**defaults)


class TestMixin(object):
    def setUp(self):
        super(TestMixin, self).setUp()
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)

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


class ReviewTestMixin(object):
    def setup_reviewer_team_and_permissions(self):
        self.review_team, unused = Team.objects.get_or_create(
            slug="financial-aid-review-team",
            name="Finaid review team")
        ct = ContentType.objects.get_for_model(FinancialAidApplication)
        perm, unused = Permission.objects.get_or_create(
            codename="review_financial_aid",
            name="Can review financial aid applications",
            content_type=ct)
        self.review_team.permissions.add(perm)

    def make_reviewer(self, user):
        self.setup_reviewer_team_and_permissions()
        Membership.objects.get_or_create(team=self.review_team,
                                         user=user,
                                         state="member")

    def make_not_reviewer(self, user):
        self.setup_reviewer_team_and_permissions()
        Membership.objects.filter(team=self.review_team,
                                  user=user).delete()
