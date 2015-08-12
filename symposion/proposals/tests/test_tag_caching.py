from django.test import TestCase
from pycon.models import PyConTalkProposal, PyConLightningTalkProposal, PyConTutorialProposal
from pycon.tests.factories import PyConTalkProposalFactory, PyConLightningTalkProposalFactory, \
    PyConTutorialProposalFactory


class TagCachingTestMixin():
    def setUp(self):
        self.proposal = self.factory()

    def test_default(self):
        self.assertEqual("", self.proposal.cached_tags)

    def test_add_one_tag(self):
        self.proposal.tags.set('huey')
        print("tags display: %s" % self.proposal.get_tags_display())
        proposal = self.model.objects.get(id=self.proposal.id)
        self.assertEqual('huey', proposal.cached_tags)

    def test_add_two_tags(self):
        self.proposal.tags.set('huey', 'dewey')
        print("tags display: %s" % self.proposal.get_tags_display())
        proposal = self.model.objects.get(id=self.proposal.id)
        self.assertEqual('huey, dewey', proposal.cached_tags)

    def test_remove_one_tag(self):
        self.proposal.tags.set('huey')
        proposal = self.model.objects.get(id=self.proposal.id)
        self.assertEqual('huey', proposal.cached_tags)
        proposal.tags.remove('huey')
        proposal = self.model.objects.get(id=self.proposal.id)
        self.assertEqual('', proposal.cached_tags)


class PyConTalkProposalTagCachingTest(TagCachingTestMixin, TestCase):
    factory = PyConTalkProposalFactory
    model = PyConTalkProposal


class PyConLightningTalkProposalTagCachingTest(TagCachingTestMixin, TestCase):
    factory = PyConLightningTalkProposalFactory
    model = PyConLightningTalkProposal


class PyConTutorialProposalTagCachingTest(TagCachingTestMixin, TestCase):
    factory = PyConTutorialProposalFactory
    model = PyConTutorialProposal


# There are other models that inherit from ProposalBase too, but testing
# a few of them should prove that it works.
