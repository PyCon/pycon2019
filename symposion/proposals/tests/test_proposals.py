from django.test import TestCase

from symposion.proposals.tests.factories import ProposalBaseFactory
from symposion.schedule.tests.factories import PresentationFactory


class ProposalsTest(TestCase):
    def test_can_edit(self):
        # If a presentation has been created, speaker can no longer edit their proposal
        prop = ProposalBaseFactory()
        self.assertTrue(prop.can_edit())
        PresentationFactory(proposal_base=prop)
        self.assertFalse(prop.can_edit())
