from django.db import models
from django.utils.translation import ugettext_lazy as _

from symposion.proposals.models import ProposalBase


class PyConProposalCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "PyCon proposal category"
        verbose_name_plural = "PyCon proposal categories"


class PyConProposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]

    STATUS_UNREVIEWED = 'unreviewed'
    STATUS_KITTENDOME = 'kittendome'
    STATUS_THUNDERDOME = 'thunderdome'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DAMAGED = 'damaged'
    STATUS_REJECTED = 'rejected'

    STATUS_OPTIONS = [
        (STATUS_UNREVIEWED, 'Not Yet Reviewed'),
        (STATUS_KITTENDOME, 'In Kittendome'),
        (STATUS_THUNDERDOME, 'In Thunderdome'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_DAMAGED, 'Damaged'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    REJECTION_POSTER = 'poster'
    REJECTION_LIGHTNING = 'lightning'
    REJECTION_MOVED = 'moved'
    REJECTION_DUPLICATE = 'duplicate'
    REJECTION_ADMIN = 'administrative'
    REJECTION_BAD = 'bad'

    REJECTION_OPTIONS = [
        (REJECTION_POSTER, 'Suggest re-submission as poster.'),
        (REJECTION_LIGHTNING, 'Suggest lightning talk.'),
        (REJECTION_MOVED, 'Re-submitted under appropriate category.'),
        (REJECTION_DUPLICATE, 'Duplicate'),
        (REJECTION_ADMIN, 'Adminstrative Action (Other)'),
        (REJECTION_BAD, "No really: rejected. It's just plain bad."),
    ]

    category = models.ForeignKey(PyConProposalCategory)
    audience_level = models.IntegerField(
        choices=AUDIENCE_LEVELS,
        help_text=_('Level of audience expertise assumed in Python.'),
        verbose_name='Python level')
    overall_status = models.CharField(
        max_length=20,
        choices=STATUS_OPTIONS,
        default=STATUS_UNREVIEWED,
        help_text=_('The status of the proposal.'))
    damaged_score = models.IntegerField(
        blank=True,
        null=True,
        help_text=_('The amount of interested in a talk.'))
    rejection_status = models.CharField(
        max_length=20,
        blank=True,
        choices=REJECTION_OPTIONS,
        help_text=_('The reason the proposal was rejected.'))
    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2014/speaking/recording/' target='_blank'>PyCon 2014 Recording Release</a> for details."
    )

    class Meta:
        abstract = True


class PyConTalkProposal(PyConProposal):

    DURATION_CHOICES = [
        (0, "No preference"),
        (1, "I prefer a 30 minute slot"),
        (2, "I prefer a 45 minute slot"),
    ]

    extreme = models.BooleanField(
        default=False,
        help_text="'Extreme' talks are advanced talks with little or no introductory material. See <a href='http://us.pycon.org/2014/speaker/extreme/' target='_blank'>Extreme Talks</a> for details."
    )
    duration = models.IntegerField(choices=DURATION_CHOICES)

    class Meta:
        verbose_name = "PyCon talk proposal"


class PyConTutorialProposal(PyConProposal):
    DOMAIN_LEVEL_NOVICE = 1
    DOMAIN_LEVEL_EXPERIENCED = 2
    DOMAIN_LEVEL_INTERMEDIATE = 3

    DOMAIN_LEVELS = [
        (DOMAIN_LEVEL_NOVICE, "Novice"),
        (DOMAIN_LEVEL_INTERMEDIATE, "Intermediate"),
        (DOMAIN_LEVEL_EXPERIENCED, "Experienced"),
    ]

    domain_level = models.IntegerField(
        choices=DOMAIN_LEVELS,
        help_text=_('Level of audience expertise assumed in the '
                    'presentation\'s domain.'))

    outline = models.TextField(
        _("Outline"),
        help_text=_("Detailed outline. Will be made public "
                    "if your talk is accepted.")
    )
    more_info = models.TextField(
        _("More info"),
        help_text=_("More info. Will be made public "
                    "if your talk is accepted.")
    )

    class Meta:
        verbose_name = "PyCon tutorial proposal"


class PyConPosterProposal(PyConProposal):
    class Meta:
        verbose_name = "PyCon poster proposal"


class PyConSponsorTutorialProposal(ProposalBase):
    class Meta:
        verbose_name = "PyCon Sponsor Tutorial proposal"

    def __unicode__(self):
        return self.title
