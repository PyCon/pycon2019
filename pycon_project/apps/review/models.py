# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models import Q

from django.contrib.auth.models import User

from biblion import creole_parser

from proposals.models import Proposal


class ProposalScoreExpression(object):

    def as_sql(self, qn, connection=None):
        sql = "((3 * plus_one + plus_zero) - (minus_zero + 3 * minus_one))"
        return sql, []

    def prepare_database_save(self, unused):
        return self


class Votes(object):
    PLUS_ONE = "+1"
    PLUS_ZERO = "+0"
    MINUS_ZERO = u"−0"
    MINUS_ONE = u"−1"

    CHOICES = [
        (PLUS_ONE, u"+1 — Good proposal and I will argue for it to be accepted."),
        (PLUS_ZERO, u"+0 — OK proposal, but I will not argue for it to be accepted."),
        (MINUS_ZERO, u"−0 — Weak proposal, but I will not argue strongly against acceptance."),
        (MINUS_ONE, u"−1 — Serious issues and I will argue to reject this proposal."),
    ]
VOTES = Votes()


class ReviewAssignment(models.Model):
    AUTO_ASSIGNED_INITIAL = 0
    OPT_IN = 1
    AUTO_ASSIGNED_LATER = 2

    ORIGIN_CHOICES = [
        (AUTO_ASSIGNED_INITIAL, "auto-assigned, initial"),
        (OPT_IN, "opted-in"),
        (AUTO_ASSIGNED_LATER, "auto-assigned, later"),
    ]

    proposal = models.ForeignKey("proposals.Proposal")
    user = models.ForeignKey(User)

    origin = models.IntegerField(choices=ORIGIN_CHOICES)

    assigned_at = models.DateTimeField(default=datetime.now)
    opted_out = models.BooleanField()

    @classmethod
    def create_assignments(cls, proposal, origin=AUTO_ASSIGNED_INITIAL):
        speakers = [proposal.speaker] + list(proposal.additional_speakers.all())
        reviewers = User.objects.exclude(
            pk__in=[
                speaker.user_id
                for speaker in speakers
                if speaker.user_id is not None
            ]
        ).filter(
            groups__name="reviewers",
        ).filter(
            Q(reviewassignment__opted_out=False) | Q(reviewassignment=None)
        ).annotate(
            num_assignments=models.Count("reviewassignment")
        ).order_by(
            "num_assignments",
        )
        for reviewer in reviewers[:3]:
            cls._default_manager.create(
                proposal=proposal,
                user=reviewer,
                origin=origin,
            )


class Review(models.Model):
    VOTES = VOTES

    proposal = models.ForeignKey("proposals.Proposal", related_name="reviews")
    user = models.ForeignKey(User)

    # No way to encode "-0" vs. "+0" into an IntegerField, and I don't feel
    # like some complicated encoding system.
    vote = models.CharField(max_length=2, blank=True, choices=VOTES.CHOICES)
    comment = models.TextField(
        help_text = "You can use <a href='http://wikicreole.org/' target='_blank'>creole</a> markup. <a id='preview' href='#'>Preview</a>",
    )
    comment_html = models.TextField(editable=False)
    submitted_at = models.DateTimeField(default=datetime.now, editable=False)

    def save(self, **kwargs):
        if self.vote:
            vote, created = LatestVote.objects.get_or_create(
                proposal = self.proposal,
                user = self.user,
                defaults = dict(
                    vote = self.vote,
                    submitted_at = self.submitted_at,
                )
            )
            if not created:
                LatestVote.objects.filter(pk=vote.pk).update(vote=self.vote)
                self.proposal.result.update_vote(self.vote, previous=vote.vote)
            else:
                self.proposal.result.update_vote(self.vote)
        self.comment_html = creole_parser.parse(self.comment)
        super(Review, self).save(**kwargs)

    def css_class(self):
        return {
            self.VOTES.PLUS_ONE: "plus-one",
            self.VOTES.PLUS_ZERO: "plus-zero",
            self.VOTES.MINUS_ZERO: "minus-zero",
            self.VOTES.MINUS_ONE: "minus-one",
        }[self.vote]


class LatestVote(models.Model):
    VOTES = VOTES

    proposal = models.ForeignKey("proposals.Proposal", related_name="votes")
    user = models.ForeignKey(User)

    # No way to encode "-0" vs. "+0" into an IntegerField, and I don't feel
    # like some complicated encoding system.
    vote = models.CharField(max_length=2, choices=VOTES.CHOICES)
    submitted_at = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        unique_together = [("proposal", "user")]

    def css_class(self):
        return {
            self.VOTES.PLUS_ONE: "plus-one",
            self.VOTES.PLUS_ZERO: "plus-zero",
            self.VOTES.MINUS_ZERO: "minus-zero",
            self.VOTES.MINUS_ONE: "minus-one",
        }[self.vote]


class ProposalResult(models.Model):
    proposal = models.OneToOneField("proposals.Proposal", related_name="result")
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    comment_count = models.PositiveIntegerField(default=1)
    vote_count = models.PositiveIntegerField(default=1)
    plus_one = models.PositiveIntegerField(default=0)
    plus_zero = models.PositiveIntegerField(default=0)
    minus_zero = models.PositiveIntegerField(default=0)
    minus_one = models.PositiveIntegerField(default=0)
    accepted = models.NullBooleanField(choices=[
        (True, "accepted"),
        (False, "rejected"),
        (None, "undecided"),
    ], default=None)

    @classmethod
    def full_calculate(cls):
        for proposal in Proposal.objects.all():
            result, created = cls._default_manager.get_or_create(proposal=proposal)
            result.comment_count = Review.objects.filter(proposal=proposal).count()
            result.vote_count = LatestVote.objects.filter(proposal=proposal).count()
            result.plus_one = LatestVote.objects.filter(
                proposal = proposal,
                vote = VOTES.PLUS_ONE
            ).count()
            result.plus_zero = LatestVote.objects.filter(
                proposal = proposal,
                vote = VOTES.PLUS_ZERO
            ).count()
            result.minus_zero = LatestVote.objects.filter(
                proposal = proposal,
                vote = VOTES.MINUS_ZERO
            ).count()
            result.minus_one = LatestVote.objects.filter(
                proposal = proposal,
                vote = VOTES.MINUS_ONE
            ).count()
            result.save()
            cls._default_manager.filter(pk=result.pk).update(score=ProposalScoreExpression())

    def update_vote(self, vote, previous=None):
        mapping = {
            VOTES.PLUS_ONE: "plus_one",
            VOTES.PLUS_ZERO: "plus_zero",
            VOTES.MINUS_ZERO: "minus_zero",
            VOTES.MINUS_ONE: "minus_one",
        }
        if previous:
            if previous == vote:
                return
            setattr(self, mapping[previous], models.F(mapping[previous]) - 1)
        setattr(self, mapping[vote], models.F(mapping[vote]) + 1)
        self.save()
        model = self.__class__
        model._default_manager.filter(pk=self.pk).update(score=ProposalScoreExpression())


class Comment(models.Model):
    proposal = models.ForeignKey("proposals.Proposal", related_name="comments")
    commenter = models.ForeignKey(User)
    text = models.TextField()

    # Or perhaps more accurately, can the user see this comment.
    public = models.BooleanField(choices=[
        (True, "public"),
        (False, "private"),
    ])
    commented_at = models.DateTimeField(default=datetime.now)
