from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from symposion.conference.models import Section
from symposion.proposals.kinds import ensure_proposal_records
from symposion.proposals.models import ProposalSection, ProposalKind
from symposion.reviews.models import Review


class TestEnsureProposalRecords(TestCase):
    def test_init(self):
        # Presumably, the records already exist since the code
        # would have been invoked post-migration during test initialization.
        # Double-check a few.
        review_ct = ContentType.objects.get_for_model(Review)
        Permission.objects.get(content_type=review_ct, codename='can_review_talks')
        Permission.objects.get(content_type=review_ct, codename='can_review_lightning-talks')

    def test_harder(self):
        # Delete a few records, run ensure_proposal_records, and make sure
        # they come back
        review_ct = ContentType.objects.get_for_model(Review)
        ProposalKind.objects.filter(slug__in=['talk', 'lightning-talk']).delete()
        ProposalSection.objects.filter(section__slug__in=['talks', 'lightning-talks']).delete()
        Section.objects.filter(slug__in=['talks', 'lightning-talks']).delete()
        Permission.objects.filter(content_type=review_ct,
                                  codename__startswith='can_review').delete()

        ensure_proposal_records()

        Permission.objects.get(content_type=review_ct, codename='can_review_talks')
        Permission.objects.get(content_type=review_ct, codename='can_review_lightning-talks')
        ProposalKind.objects.get(slug='talk')
