import datetime

from django.db import models
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType

from markitup.fields import MarkupField

from symposion.conference.models import Section


class ProposalSection(models.Model):
    """
    configuration of proposal submissions for a specific Section.
    
    a section is available for proposals iff:
      * it is after start (if there is one) and
      * it is before end (if there is one) and
      * closed is NULL or False
    """
    
    section = models.OneToOneField(Section)
    
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    closed = models.NullBooleanField()
    published = models.NullBooleanField()
    
    @classmethod
    def available(cls):
        now = datetime.datetime.now()
        return cls._default_manager.filter(
            Q(start__lt=now) | Q(start=None),
            Q(end__gt=now) | Q(end=None),
            Q(closed=False) | Q(closed=None),
        )
    
    def __unicode__(self):
        return self.section.name


class ProposalKind(models.Model):
    """
    e.g. talk vs panel vs tutorial vs poster
    
    Note that if you have different deadlines, reviewers, etc. you'll want
    to distinguish the section as well as the kind.
    """
    
    section = models.ForeignKey(Section)
    
    name = models.CharField("name", max_length=100)
    slug = models.SlugField()
    
    # content type of ProposalBase sub-class
    proposal_model = models.ForeignKey(ContentType)
    
    def __unicode__(self):
        return self.name


class ProposalBase(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "If your talk is accepted this will be made public and printed in the program. Should be one paragraph, maximum 400 characters."
    )
    abstract = MarkupField(
        help_text = "Detailed description and outline. Will be made public if your talk is accepted. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>."
    )
    additional_notes = MarkupField(
        blank=True,
        help_text = "Anything else you'd like the program committee to know when making their selection: your past speaking experience, open source community experience, etc. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>."
    )
    submitted = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False,
    )
    speaker = models.ForeignKey("speakers.Speaker", related_name="proposals")
    additional_speakers = models.ManyToManyField("speakers.Speaker", blank=True)
    cancelled = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
    
    def can_edit(self):
        return True
    
    @property
    def speaker_email(self):
        return self.speaker.email

    @property
    def number(self):
        return str(self.pk).zfill(3)
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker


# @@@ the following should go under pycon


class PyConProposalCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.name


class PyConProposal(ProposalBase):
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]

    DURATION_CHOICES = [
        (0, "No preference"),
        (1, "I prefer a 30 minute slot"),
        (2, "I prefer a 45 minute slot"),
    ]
    
    category = models.ForeignKey(PyConProposalCategory)
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    extreme = models.BooleanField(
        default=False,
        help_text = "'Extreme' talks are advanced talks with little or no introductory material. See <a href='http://us.pycon.org/2012/speaker/extreme/' target='_blank'>http://us.pycon.org/2012/speaker/extreme/</a> for details."
    )
    duration = models.IntegerField(choices=DURATION_CHOICES)
