import random
from collections import defaultdict
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models import Q

from symposion.reviews.models import ProposalGroup, ReviewAssignment
from symposion.teams.models import Team
from symposion.utils.mail import send_email


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--proposal-group-name",
            help="Which proposal group to assign reviewers for",
        ),
        make_option(
            '--new-reviewers',
            action="store_true",
            default=False,
            help=(
                "Only assign talks to people who don't have any review "
                "assignments yet"
            ),
        )
    )

    def handle(self, *args, **options):
        group = ProposalGroup.objects.get(
            name=options["proposal_group_name"],
        )
        reviewers = self.get_reviewers()
        if options['new_reviewers']:
            user_reviews = self.assign_new_user_reviews(group, reviewers)
        else:
            user_reviews = self.assign_user_reviews(group, reviewers)

        for user, proposal_results in user_reviews.iteritems():
            print("Sending assignments to %r" % user.email)
            for pr in proposal_results:
                ReviewAssignment.objects.get_or_create(
                    proposal=pr.proposal,
                    user=user,
                    origin=ReviewAssignment.AUTO_ASSIGNED_INITIAL,
                )
            send_email([user.email], "new_review_assignments", context={
                "user": user,
                "proposal_results": proposal_results,
                "proposal_group": group,
            })

    def assign_user_reviews(self, group, reviewers):
        user_reviews = defaultdict(list)
        for proposal_result in group.proposal_results.all():
            proposal_reviewers = random.sample([
                user for user in reviewers
                if user.id not in self.proposal_speaker_user_ids(proposal_result.proposal)
            ], 7)
            for reviewer in proposal_reviewers:
                user_reviews[reviewer].append(proposal_result)
        return user_reviews

    def assign_new_user_reviews(self, group, reviewers):
        proposal_results = group.proposal_results.all()
        assigned_reviewer_ids = set(ReviewAssignment.objects.filter(
            proposal_id__in=proposal_results.values_list("proposal_id", flat=True),
        ).values_list("user_id", flat=True))
        reviewers = [
            user for user in reviewers
            if user.id not in assigned_reviewer_ids
        ]
        user_reviews = {}
        for user in reviewers:
            user_reviews[user] = random.sample([
                proposal_result
                for proposal_result in proposal_results
                if user.id not in self.proposal_speaker_user_ids(proposal_result.proposal)
            ], 15)
        return user_reviews

    def get_reviewers(self):
        teams = Team.objects.filter(
            permissions__codename="can_review_talks"
        )
        memberships = set()
        for team in teams:
            memberships.update(team.memberships.filter(
                Q(state="member") | Q(state="manager")
            ).select_related("user"))
        return [
            membership.user
            for membership in memberships
            if membership.user.email
        ]

    def proposal_speaker_user_ids(self, proposal):
        speakers = [proposal.speaker] + list(proposal.additional_speakers.all())
        return [speaker.user_id for speaker in speakers if speaker.user_id is not None]
