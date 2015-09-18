from httplib import OK
from unittest import SkipTest

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission

from pycon.tests.factories import PyConTalkProposalFactory, PyConTutorialProposalFactory, \
    ProposalResultFactory
from symposion.proposals.models import ProposalBase, ProposalKind
from symposion.proposals.tests.factories import init_kinds
from symposion.reviews.models import Review, ReviewAssignment, Votes
from symposion.reviews.views import is_voting_period_active


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class ReviewTestMixin(object):
    def setUp(self):
        super(ReviewTestMixin, self).setUp()
        init_kinds()

    def create_user(self, username="joe",
                    email=None,
                    password="snoopy",
                    first_name="Joe",
                    last_name="Smith"
                    ):
        if email is None:
            email = "%s@example.com" % username
        return User.objects.create_user(username,
                                        email=email,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name)

    def login(self, username="joe@example.com", password="snoopy"):
        # The auth backend that pycon is using is kind of gross. It expects
        # username to contain the email address.
        self.assertTrue(self.client.login(username=username,
                                          password=password),
                        "Login failed")


class ReviewTests(TestCase):
    fixtures = ["proposals"]

    def setUp(self):
        raise SkipTest

    def get(self, url_name, *args, **kwargs):
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs))

    def post(self, url_name, *args, **kwargs):
        data = kwargs.pop("data")
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs),
                                data)

    def login(self, user, password):
        return login(self, user, password)

    def test_detail_perms(self):
        guidos_proposal = ProposalBase.objects.all()[0]
        response = self.get("review_detail", pk=guidos_proposal.pk)

        # Not logged in
        self.assertEqual(response.status_code, 302)

        with self.login("guido", "pythonisawesome"):
            response = self.get("review_detail", pk=guidos_proposal.pk)
            # Guido can see his own proposal.
            self.assertEqual(response.status_code, 200)

        with self.login("matz", "pythonsucks"):
            response = self.get("review_detail", pk=guidos_proposal.pk)
            # Matz can't see guido's proposal
            self.assertEqual(response.status_code, 302)

        larry = User.objects.get(username="larryw")
        # Larry is a trustworthy guy, he's a reviewer.
        larry.groups.add(Group.objects.get(name="reviewers"))
        with self.login("larryw", "linenoisehere"):
            response = self.get("review_detail", pk=guidos_proposal.pk)
            # Reviewers can see a review detail page.
            self.assertEqual(response.status_code, 200)

    def test_reviewing(self):
        guidos_proposal = ProposalBase.objects.all()[0]

        with self.login("guido", "pythonisawesome"):
            response = self.post("review_review", pk=guidos_proposal.pk, data={
                "vote": "+1",
            })
            # It redirects, but...
            self.assertEqual(response.status_code, 302)
            # ... no vote recorded
            self.assertEqual(guidos_proposal.reviews.count(), 0)

        larry = User.objects.get(username="larryw")
        # Larry is a trustworthy guy, he's a reviewer.
        larry.groups.add(Group.objects.get(name="reviewers"))
        with self.login("larryw", "linenoisehere"):
            response = self.post("review_review", pk=guidos_proposal.pk, data={
                "vote": "+0",
                "text": "Looks like a decent proposal, and Guido is a smart guy",
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(guidos_proposal.reviews.count(), 1)
            self.assertEqual(ReviewAssignment.objects.count(), 1)
            assignment = ReviewAssignment.objects.get()
            self.assertEqual(assignment.proposal, guidos_proposal)
            self.assertEqual(assignment.origin, ReviewAssignment.OPT_IN)
            self.assertEqual(guidos_proposal.comments.count(), 1)
            comment = guidos_proposal.comments.get()
            self.assertFalse(comment.public)

            response = self.post("review_review", pk=guidos_proposal.pk, data={
                "vote": "+1",
                "text": "Actually Perl is dead, we really need a talk on the future",
            })
            self.assertEqual(guidos_proposal.reviews.count(), 2)
            self.assertEqual(ReviewAssignment.objects.count(), 1)
            assignment = ReviewAssignment.objects.get()
            self.assertEqual(assignment.review, Review.objects.order_by("-id")[0])
            self.assertEqual(guidos_proposal.comments.count(), 2)

            # Larry's a big fan...
            response = self.post("review_review", pk=guidos_proposal.pk, data={
                "vote": "+20",
            })
            self.assertEqual(guidos_proposal.reviews.count(), 2)

    def test_speaker_commenting(self):
        guidos_proposal = ProposalBase.objects.all()[0]

        with self.login("guido", "pythonisawesome"):
            response = self.get("review_comment", pk=guidos_proposal.pk)
            # Guido can comment on his proposal.
            self.assertEqual(response.status_code, 200)

            response = self.post("review_comment", pk=guidos_proposal.pk, data={
                "text": "FYI I can do this as a 30-minute or 45-minute talk.",
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(guidos_proposal.comments.count(), 1)
            comment = guidos_proposal.comments.get()
            self.assertTrue(comment.public)

        larry = User.objects.get(username="larryw")
        # Larry is a trustworthy guy, he's a reviewer.
        larry.groups.add(Group.objects.get(name="reviewers"))
        with self.login("larryw", "linenoisehere"):
            response = self.get("review_comment", pk=guidos_proposal.pk)
            # Larry can comment, since he's a reviewer
            self.assertEqual(response.status_code, 200)

            response = self.post("review_comment", pk=guidos_proposal.pk, data={
                "text": "Thanks for the heads-up Guido."
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(guidos_proposal.comments.count(), 2)

        with self.login("matz", "pythonsucks"):
            response = self.get("review_comment", pk=guidos_proposal.pk)
            # Matz can't comment.
            self.assertEqual(response.status_code, 302)


class ReviewPageTest(ReviewTestMixin, TestCase):
    fixtures = [
        'conference.json',
        'proposal_base.json',
    ]

    def test_review_section(self):

        talk = PyConTalkProposalFactory(
            title="My talk",
            description="Description of the talk",
            category__name="My talk category"
        )
        # Make a few more talks to inflate the queries if we haven't optimized them properly
        for __ in range(10):
            ProposalResultFactory(proposal=PyConTalkProposalFactory())
        tutorial = PyConTutorialProposalFactory(
            title="My tutorial",
            category__name="My tutorial category"
        )

        self.user = self.create_user()
        self.login()

        # If we go to the talk section, we only see talk data (not
        # tutorial data).
        kind = ProposalKind.objects.get(slug='talk')
        section = kind.section
        url = reverse('review_section', kwargs={'section_slug': section.slug})
        ct = ContentType.objects.get_for_model(Review)
        perm, __ = Permission.objects.get_or_create(
            codename="can_review_%s" % section.slug,
            content_type=ct,
        )
        self.user.user_permissions.add(perm)

        # Run it once to force creation of result objects
        rsp = self.client.get(url)
        self.assertEqual(OK, rsp.status_code)

        # Now run it for the test, making sure we don't need more queries than reasonable
        with self.assertNumQueries(16):
            rsp = self.client.get(url)
        self.assertEqual(OK, rsp.status_code)
        self.assertContains(rsp, talk.title)
        self.assertContains(rsp, "My talk category")
        self.assertNotContains(rsp, tutorial.title)
        self.assertNotContains(rsp, "My tutorial category")

        # Now make sure the tutorial section has tutorial data but not talk.
        kind2 = ProposalKind.objects.get(slug='tutorial')
        section = kind2.section
        perm, __ = Permission.objects.get_or_create(
            codename="can_review_%s" % section.slug,
            content_type=ct,
        )
        self.user.user_permissions.add(perm)
        url = reverse('review_section', kwargs={'section_slug': section.slug})
        rsp = self.client.get(url)
        self.assertEqual(OK, rsp.status_code)
        self.assertNotContains(rsp, talk.title)
        self.assertNotContains(rsp, "My talk category")
        self.assertContains(rsp, tutorial.title)
        self.assertContains(rsp, "My tutorial category")


class SubmitReviewTest(ReviewTestMixin, TestCase):
    fixtures = [
        'conference.json',
        'proposal_base.json',
    ]

    def submit_review(self, proposal, user, vote):
        # Submit a vote and return the updated proposal object
        assert is_voting_period_active(proposal)
        self.login(username=user.username)
        url = reverse('review_detail', kwargs={'pk': proposal.pk})
        data = dict(
            vote_submit="yep",
            vote=vote,
            comment="deep thoughts",
        )
        rsp = self.client.post(url, data)
        self.assertRedirects(rsp, url)
        return type(proposal).objects.get(pk=proposal.pk)

    def test_submit_review(self):
        # Reviewers can submit multiple reviews. Only their most recent vote counts.
        talk = PyConTalkProposalFactory(title="talk", description="talk",
                                        category__name="My talk category")
        self.user = self.create_user()
        perm, __ = Permission.objects.get_or_create(
            codename="can_review_talks",
            content_type=ContentType.objects.get_for_model(Review),
        )
        self.user.user_permissions.add(perm)
        user2 = self.create_user(username="user2")
        user2.user_permissions.add(perm)

        # User submits first vote: +1
        talk = self.submit_review(talk, self.user, "+1")
        # One +1 vote gives a score of 3
        self.assertEqual(3, talk.result.score)

        # Let's try adding another vote - because it's from the same
        # user, it should supersede their previous vote in the score.
        talk = self.submit_review(talk, self.user, Votes.MINUS_ZERO)
        # A -0 vote is a score of -1
        self.assertEqual(-1, talk.result.score)

        # Now, add a vote from a different user, which should be counted
        # separately and adjust the score
        talk = self.submit_review(talk, user2, "+1")
        # Adding a new +1 vote adds 3 to the previous score
        self.assertEqual(2, talk.result.score)
