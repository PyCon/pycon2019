from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from symposion.proposals.models import ProposalBase


class PyConProposalCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "PyCon proposal category"
        verbose_name_plural = "PyCon proposal categories"


class ThunderdomeGroup(models.Model):
    """A set of talk proposals, grouped together for consideration within
    thunderdome.
    """
    label = models.CharField(max_length=250)
    code = models.CharField(max_length=20, unique=True)
    decided = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def as_dict(self):
        return {
            'code': self.code,
            'decided': self.decided,
            'label': self.label,
            'talks': [i.as_dict() for i in self.talks.order_by('id')],
        }


class PyConProposal(ProposalBase):
    # ABSTRACT MODEL
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, _(u"Novice")),
        (AUDIENCE_LEVEL_INTERMEDIATE, _(u"Intermediate")),
        (AUDIENCE_LEVEL_EXPERIENCED, _(u"Experienced")),
    ]

    STATUS_UNREVIEWED = 1
    STATUS_KITTENDOME = 2
    STATUS_THUNDERDOME = 3
    STATUS_ACCEPTED = 4
    STATUS_DAMAGED = 5
    STATUS_REJECTED = 6

    STATUS_OPTIONS = [
        (STATUS_UNREVIEWED, 'Not Yet Reviewed'),
        (STATUS_KITTENDOME, 'In Kittendome'),
        (STATUS_THUNDERDOME, 'In Thunderdome'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_DAMAGED, 'Damaged'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    REJECTION_POSTER = 1
    REJECTION_LIGHTNING = 2
    REJECTION_MOVED = 3
    REJECTION_DUPLICATE = 4
    REJECTION_ADMIN = 5
    REJECTION_BAD = 6

    REJECTION_OPTIONS = [
        (REJECTION_POSTER, 'Suggest re-submission as poster.'),
        (REJECTION_LIGHTNING, 'Suggest lightning talk.'),
        (REJECTION_MOVED, 'Re-submitted under appropriate category.'),
        (REJECTION_DUPLICATE, 'Duplicate'),
        (REJECTION_ADMIN, 'Administrative Action (Other)'),
        (REJECTION_BAD, "No really: rejected. It's just plain bad."),
    ]

    category = models.ForeignKey(PyConProposalCategory)
    audience_level = models.IntegerField(
        choices=AUDIENCE_LEVELS,
        help_text=_(u'Level of audience expertise assumed in Python.'),
        verbose_name=_(u'Python level'))
    overall_status = models.IntegerField(
        choices=STATUS_OPTIONS,
        default=STATUS_UNREVIEWED,
        help_text=_(u'The status of the proposal.'))
    damaged_score = models.IntegerField(
        blank=True,
        null=True,
        help_text=_(u"Numerical indicator of the amount of interest in a talk set to 'damaged' status."))
    rejection_status = models.IntegerField(
        blank=True,
        null=True,
        choices=REJECTION_OPTIONS,
        help_text=_(u'The reason the proposal was rejected.'))
    recording_release = models.BooleanField(
        default=True,
        help_text=_(u"By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2016/speaking/recording/' target='_blank'>PyCon 2016 Recording Release</a> for details.")
    )

    additional_requirements = models.TextField(
        _(u"Additional requirements"),
        blank=True,
        help_text=_(u"Please let us know if you have any specific needs (A/V requirements, multiple microphones, a table, etc).  Note for example that 'audio out' is not provided for your computer unless you tell us in advance.")
    )

    class Meta:
        abstract = True


class PyConTalkProposal(PyConProposal):

    DURATION_CHOICES = [
        (0, _(u"No preference")),
        (1, _(u"I prefer a 30 minute slot")),
        (2, _(u"I prefer a 45 minute slot")),
    ]

    duration = models.IntegerField(choices=DURATION_CHOICES)

    outline = models.TextField(
        _(u"Outline")
    )
    audience = models.CharField(
        max_length=150,
        help_text=_(u'Who is the intended audience for your talk? (Be '
                    u'specific; "Python programmers" is not a good answer '
                    u'to this question.)'),
    )
    perceived_value = models.TextField(
        _(u"Objectives"),
        max_length=400,
        help_text=_(u"What will attendees get out of your talk? When they "
                    u"leave the room, what will they know that they didn't "
                    u"know before?"),
    )

    thunderdome_group = models.ForeignKey(ThunderdomeGroup,
        blank=True,
        default=None,
        null=True,
        related_name=u'talks',
    )

    class Meta:
        verbose_name = "PyCon talk proposal"

    def as_dict(self, details=False):
        answer = super(PyConTalkProposal, self).as_dict(details=details)
        if details:
            code = None
            if self.thunderdome_group:
                code = self.thunderdome_group.code
            answer['thunderdome_group'] = code
        return answer


class PyConLightningTalkProposal(PyConProposal):

    class Meta:
        verbose_name = "PyCon lightning talk proposal"


class PyConTutorialProposal(PyConProposal):
    DOMAIN_LEVEL_NOVICE = 1
    DOMAIN_LEVEL_EXPERIENCED = 2
    DOMAIN_LEVEL_INTERMEDIATE = 3

    DOMAIN_LEVELS = [
        (DOMAIN_LEVEL_NOVICE, _(u"Novice")),
        (DOMAIN_LEVEL_INTERMEDIATE, _(u"Intermediate")),
        (DOMAIN_LEVEL_EXPERIENCED, _(u"Experienced")),
    ]

    domain_level = models.IntegerField(
        choices=DOMAIN_LEVELS,
        help_text=_(u'Level of audience expertise assumed in the '
                    u'presentation\'s domain.'))

    outline = models.TextField(
        _(u"Outline")
    )
    more_info = models.TextField(
        _(u"More info"),
        help_text=_(u"More info. Will be made public "
                    u"if your talk is accepted.")
    )
    audience = models.CharField(
        max_length=150,
        help_text=_(u'Who is the intended audience for your talk? (Be '
                    u'specific; "Python programmers" is not a good answer '
                    u'to this question.)'),
    )
    perceived_value = models.TextField(
        _(u"Objectives"),
        max_length=500,
        help_text=_(u"What will attendees get out of your talk? When they "
                    u"leave the room, what will they know that they didn't "
                    u"know before?"),
    )
    handout = models.FileField(
        _(u"Student Handout"),
        blank=True,
        null=True,
        help_text=_(u'Upload a resource to be distributed to students  '
                    u'attending the tutorial session.'),
        upload_to="tutorial_handouts"
    )

    # Populated by update_tutorial_registrant command.
    registrants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, editable=False,
        help_text=_(u'CTE registered participants for this tutorial.'))
    registration_count = models.IntegerField(
        default=0, editable=False,
        help_text=_(u"Count of attendees. Allows inclusion of folks who don't "
                    "have a PyCon account."))
    max_attendees = models.IntegerField(
        blank=True, null=True, editable=False,
        help_text=_(u'Maximum number of attendees, per CTE data'))

    class Meta:
        verbose_name = "PyCon tutorial proposal"


class PyConPosterProposal(PyConProposal):
    class Meta:
        verbose_name = "PyCon Poster proposal"


class PyConSponsorTutorialProposal(ProposalBase):
    class Meta:
        verbose_name = "PyCon Sponsor Tutorial proposal"

    def __unicode__(self):
        return self.title


class PyConOpenSpaceProposal(PyConProposal):
    class Meta:
        verbose_name = "PyCon Open Space proposal"
