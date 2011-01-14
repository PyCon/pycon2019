from django.core.management.base import BaseCommand

from review.models import ProposalResult, promote_proposal


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        accepted_proposals = ProposalResult.objects.filter(accepted=True)
        
        for result in accepted_proposals:
            promote_proposal(result.proposal)
