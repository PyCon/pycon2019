import random

from django.core.management.base import BaseCommand

from symposion.reviews.models import ProposalResult, ProposalGroup


class Command(BaseCommand):
    def handle(self, *args, **options):
        prs = ProposalResult.objects.filter(
            proposal__kind__slug="talk",
            group=None
        )
        groups = list(ProposalGroup.objects.all())
        for pr in prs:
            pr.group = random.choice(groups)
            pr.save()
