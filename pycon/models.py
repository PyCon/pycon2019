# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from django_cryptography.fields import encrypt

from easy_thumbnails.signals import saved_file

from pycon import tasks

from symposion.proposals.kinds import register_proposal_model
from symposion.proposals.models import ProposalBase

SECURE_SUBMISSION_TYPE_FINAID_REIMBURSE_DETAILS = 1
SECURE_SUBMISSION_TYPE_TUTORIAL_PAYMENT_DETAILS = 2
SECURE_SUBMISSION_TYPE_TUTORIAL_TAX_FORM = 3
SECURE_SUBMISSION_TYPE_CHOICES = (
    (SECURE_SUBMISSION_TYPE_FINAID_REIMBURSE_DETAILS, _(u"Financial Aid Recipient - Reimbursement Method Details (Bank, ACH, PayPal, or similar)")),
    (SECURE_SUBMISSION_TYPE_TUTORIAL_PAYMENT_DETAILS, _(u"Tutorial Presenter - Payment Details (Bank, ACH, PayPal, or similar)")),
    (SECURE_SUBMISSION_TYPE_TUTORIAL_TAX_FORM, _(u"Tutorial Presenter - Tax Form (W-9, W-8, or similar form)")),
)


def strip(text):
    return u' '.join(text.strip().split())


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

    category = models.ForeignKey(PyConProposalCategory,
                                 blank=True, null=True)
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
        help_text=_(u"Numerical indicator of the amount of interest in a talk set "
                    u"to 'damaged' status."))
    rejection_status = models.IntegerField(
        blank=True,
        null=True,
        choices=REJECTION_OPTIONS,
        help_text=_(u'The reason the proposal was rejected.'))
    recording_release = models.BooleanField(
        default=True,
        help_text=_(u"By submitting your proposal, you agree to give permission to "
                    u"the Python Software Foundation to record, edit, and release audio "
                    u"and/or video of your presentation. If you do not agree to this, "
                    u"please uncheck this box. See "
                    u"<a href='/2019/speaking/recording/' "
                    u"target='_blank'>PyCon 2019 Recording Release</a> for details.")
    )

    additional_requirements = models.TextField(
        _(u"Additional requirements"),
        blank=True,
        help_text=_(u"Please let us know if you have any specific needs (A/V requirements, "
                    u"multiple microphones, a table, etc).  Note for example that 'audio out' "
                    u"is not provided for your computer unless you tell us in advance.")
    )

    class Meta:
        abstract = True


class PyConTalkProposal(PyConProposal):

    DURATION_CHOICES = [
        (0, _(u"No preference")),
        (1, _(u"I prefer a 30 minute slot")),
        (2, _(u"I prefer a 45 minute slot")),
    ]

    duration = models.IntegerField(
        choices=DURATION_CHOICES,
        default=1,
        help_text=strip(
            u"""
            <i>Committee note:</i>
            There are far fewer 45 minute slots available
            than 30 minute slots,
            so not every accepted talk that requests a longer slot
            may be able to get it.
            If you select a 45 minute slot,
            please indicate in your outline (below)
            what content could be cut — if possible — for a 30 minute version.
            """
        ),
    )

    outline = models.TextField(
        help_text=strip(
            u"""
            The “outline” is a skeleton of your talk that is as detailed as
            possible, including rough timings or estimates for different
            sections. If requesting a 45 minute slot, please describe what
            content would appear in the 45 minute version but not a 30 minute
            version, either within the outline or in a paragraph at the
            end.<br>
            <br>
            <i>Committee note:</i> The outline is extremely important for the
            program committee to understand what the content and structure of
            your talk will be. The timings/percentages help us compare multiple
            talks that might have a similar abstract. We know that they are
            estimates and only capture your view at this moment in time and are
            likely to change before PyCon. We hope that writing the outline is
            helpful to you as well, to organize and clarify your thoughts for
            your talk! The outline will not be shared with conference
            attendees.<br>
            <br>
            If there’s too much to your topic to cover even in 45 minutes, you
            may wish to narrow it down. Alternatively, consider submitting a
            3-hour PyCon tutorial instead. If you plan to do live coding during
            your talk, please describe your backup plan in case the live coding
            fails (for whatever reason). Suggestions include a pre-recorded
            video, or slides to replace the live coding.
            """
        ),
    )
    audience = models.TextField(
        u"Who and Why (Audience)",
        help_text=strip(
            u"""
            1–2 paragraphs that should answer three questions:
            (1) Who is this talk for?
            (2) What background knowledge or experience
            do you expect the audience to have?
            (3) What do you expect the audience to learn or do
            after watching the talk?<br>
            <br>
            <i>Committee note:</i> The “Audience” section
            helps the program committee get a sense
            of whether your talk is geared more at novices
            or experienced individuals in a given subject.
            (We need a balance of both lower-level and advanced talks
            to make a great PyCon!)
            It also helps us evaluate the relevance of your talk
            to the Python community.
            """
        ),
    )

    # TODO: this does not actually remove the fields, so the form cannot
    # yet be submitted successfully.  Should we upgrade to Django 1.10?
    # abstract = None
    # additional_requirements = None
    # audience_level = None
    # category = None
    # perceived_value = None

    class Meta:
        verbose_name = "PyCon talk proposal"

    def as_dict(self, details=False):
        answer = super(PyConTalkProposal, self).as_dict(details=details)
        if details:
            answer['duration'] = self.get_duration_display()
            answer['outline'] = self.outline
            answer['audience'] = self.audience
            answer['recording_release'] = self.recording_release
        return answer


register_proposal_model('talk', PyConTalkProposal, 'Talks')

class PyConCharlaProposal(PyConTalkProposal):

    class Meta:
        verbose_name = "PyCon Charlas proposal"

register_proposal_model('charla', PyConCharlaProposal, 'Charlas')


class PyConLightningTalkProposal(PyConProposal):

    class Meta:
        verbose_name = "PyCon lightning talk proposal"


register_proposal_model('lightning-talk', PyConLightningTalkProposal, 'Lightning Talks')


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

    audience = models.TextField(
        u"Audience",
        help_text=strip(
            u"""
            1–2 paragraphs that should answer three questions:
            (1) Who is this tutorial for?
            (2) What background knowledge or experience
            do you expect students to have?
            (3) What do you expect students to learn,
            or to be able to do after attending your tutorial?
            """
        ),
    )
    outline = models.TextField()
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


register_proposal_model('tutorial', PyConTutorialProposal, 'Tutorials')


class PyConPosterProposal(PyConProposal):
    class Meta:
        verbose_name = "PyCon Poster proposal"


register_proposal_model('poster', PyConPosterProposal, 'Posters')


class PyConSponsorTutorialProposal(ProposalBase):
    class Meta:
        verbose_name = "PyCon Sponsor Tutorial proposal"

    def __unicode__(self):
        return self.title


register_proposal_model('sponsor-tutorial', PyConSponsorTutorialProposal, 'Sponsor Tutorials')


class EduSummitTalkProposal(PyConProposal):
    class Meta:
        verbose_name = "Python Education Summit talk proposal"


register_proposal_model('edusummit', EduSummitTalkProposal, 'Education Summit')


class PyConOpenSpaceProposal(PyConProposal):
    class Meta:
        verbose_name = "PyCon Open Space proposal"


register_proposal_model('open-space', PyConOpenSpaceProposal, 'Open Spaces')


class ScheduledEvent(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    location = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(help_text="markdown")
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "PyCon Scheduled Event"

    def get_absolute_url(self):
        return reverse('scheduled_event', kwargs={'slug': self.slug})

@receiver(saved_file)
def generate_thumbnails_async(sender, fieldfile, **kwargs):
    tasks.generate_thumbnails.delay(
        model=sender, pk=fieldfile.instance.pk,
        field=fieldfile.field.name)


class PyConStartupRowApplication(models.Model):
    accepted = models.BooleanField(default=False)
    applicant_name = models.CharField(max_length=100)
    applicant_company_role = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    company_url = models.CharField(max_length=100, blank=True, default='')
    company_location = models.CharField(max_length=100)
    company_activity = models.TextField(max_length=500)
    company_python_usage = models.TextField(max_length=500)
    company_age = models.CharField(max_length=50)
    company_size = models.CharField(max_length=50)
    company_competitive_advantage = models.TextField(max_length=500)
    company_monetization_strategy = models.TextField(max_length=500)
    company_funding = models.CharField(max_length=100, blank=True, default='')
    company_additional_notes = models.TextField(max_length=500, blank=True, default='')
    company_demo_url = models.CharField(max_length=100, blank=True, default='')
    company_logo = models.ImageField(
        _(u"Company logo"),
        help_text=_("For display on our website. High resolution PNG or JPG, smallest dimension no less than 256px"),
        upload_to="startuprow_logos",
        null=True,
    )

    applicant = models.OneToOneField(User, related_name="startuprow_application", verbose_name=_("applicant"), null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
        null=True,
    )

    class Meta:
        verbose_name = "PyCon Startup Row Application"


class PyConRoomSharingOffer(models.Model):
    user = models.OneToOneField(User, related_name="room_sharing_offer", null=True, on_delete=models.SET_NULL)
    arrive = models.DateField()
    depart = models.DateField()
    contact_info = models.CharField(max_length=128)
    additional_info = models.CharField(max_length=512)
    approved = models.BooleanField(default=True)


class PyConRoomSharingRequest(models.Model):
    user = models.OneToOneField(User, related_name="room_sharing_request", null=True, on_delete=models.SET_NULL)
    arrive = models.DateField()
    depart = models.DateField()
    contact_info = models.CharField(max_length=128)
    additional_info = models.CharField(max_length=512)
    approved = models.BooleanField(default=True)

class SecureSubmission(models.Model):
    class Meta:
        permissions = (("can_view_secure_submissions", "View Secure Submissions"),)

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="secure_submissions", null=False)
    submission_type = models.IntegerField(
        choices=SECURE_SUBMISSION_TYPE_CHOICES,
        verbose_name="Submission Type",
        blank=False, null=False,
    )
    description = models.CharField(max_length=1024, blank=False, null=False, default='No description provided')
    message = encrypt(models.TextField(blank=True, null=True, default=None))
    file_attachment = encrypt(models.BinaryField(blank=True, null=True, default=None))
    file_attachment_name = models.CharField(max_length=2048, blank=True, null=True, default=None)
    file_attachment_content_type = models.CharField(max_length=2048, blank=True, null=True, default=None)
    logged = models.BooleanField(default=False, null=False, blank=True)

    @property
    def attachment_url(self):
        return reverse('secure_submission_file_retrieval', kwargs={'secure_submission_id': self.id})
