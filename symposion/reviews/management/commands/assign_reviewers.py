import random
from collections import defaultdict
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from symposion.reviews.models import ProposalGroup, ReviewAssignment
from symposion.utils.mail import send_email


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--proposal-group-name",
            help="Which proposal group to assign reviewers for",
        ),
    )

    def handle(self, *args, **options):
        group = ProposalGroup.objects.get(
            name=options["proposal_group_name"],
        )
        reviewers = list(User.objects.filter(
            groups__name="reviewers",
        ))
        user_reviews = defaultdict(list)
        for proposal_result in group.proposal_results.all():
            proposal_reviewers = random.sample([
                user for user in reviewers
                if user.id not in self.proposal_speaker_user_ids(proposal_result.proposal)
            ], 7)
            for reviewer in proposal_reviewers:
                user_reviews[reviewer].append(proposal_result)

        for user, proposal_results in user_reviews.iteritems():
            for pr in proposal_results:
                ReviewAssignment.objects.create(
                    proposal=pr.proposal,
                    user=user,
                    origin=ReviewAssignment.AUTO_ASSIGNED_INITIAL,
                )
            send_email([user.email], "new_review_assignments", context={
                "user": user,
                "proposal_results": proposal_results,
                "proposal_group": group,
            })



    def proposal_speaker_user_ids(self, proposal):
        speakers = [proposal.speaker] + list(proposal.additional_speakers.all())
        return [speaker.user_id for speaker in speakers if speaker.user_id is not None]
