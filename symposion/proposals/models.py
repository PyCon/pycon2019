# -*- coding: utf-8 -*-

import datetime
import json
import os
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

import reversion
from model_utils.managers import InheritanceManager
from taggit.managers import TaggableManager

from symposion.conference.models import Section


def strip(text):
    return u' '.join(text.strip().split())


class ProposalSection(models.Model):
    """
    configuration of proposal submissions for a specific Section.

    a section is available for proposals iff:
      * it is after start (if there is one) and
      * it is before end (if there is one) and
      * closed is NULL or False
    """

    section = models.OneToOneField(Section)

    start = models.DateTimeField(null=True, blank=True,
                                 help_text=_("When submissions open"))
    end = models.DateTimeField(null=True, blank=True,
                               help_text=_("When submissions close"))
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

    def is_available(self):
        if self.closed:
            return False
        now = datetime.datetime.now()
        if self.start and self.start > now:
            return False
        if self.end and self.end < now:
            return False
        return True

    def __unicode__(self):
        return self.section.name


class ProposalKind(models.Model):
    """
    e.g. talk vs panel vs tutorial vs poster

    Note that if you have different deadlines, reviewers, etc. you'll want
    to distinguish the section as well as the kind.
    """

    section = models.ForeignKey(Section, related_name="proposal_kinds")

    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(
        help_text="kind slugs are lowercase and singular, e.g. 'tutorial'",
        unique=True
    )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.section.slug != self.slug + "s":
            raise ValueError("section slug %s should be kind slug %s with an 's' added"
                             % (self.section.slug, self.slug))
        super(ProposalKind, self).save(*args, **kwargs)


class ProposalBase(models.Model):

    objects = InheritanceManager()

    kind = models.ForeignKey(ProposalKind)

    title = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        _("Description"),
        help_text=strip(
            u"""
            Both your title and this description are made public
            and displayed in the conference program
            to help attendees decide
            whether they are interested in this presentation.
            Limit this description to a few concise paragraphs.
            """
        ),
    )
    abstract = models.TextField(
        _("Detailed Abstract"),
        blank=True,
        help_text=_("Detailed description. Will be made public "
                    "if your talk is accepted.")
    )
    additional_notes = models.TextField(
        blank=True,
        help_text=strip(
            u"""
            Anything else you would like to share with the committee:<br>
            <b>Please do not submit any personally identifiable information.</b>
            The initial round of reviews are annonymous, and this field will
            visible to reviewers.<br>
            Speaker public speaking experience.<br>
            Speaker subject matter experience.<br>
            Have the speaker(s) given this presentation before elsewhere?<br>
            Links to recordings, slides, blog posts, code, or other material.
            <br>
            Specific needs or special requests — accessibility,
            audio (will you need to play pre-recorded sound?),
            or restrictions on when your talk can be scheduled.
            """,
        ),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
        null=True,
    )
    submitted = models.BooleanField(
        default=False
    )
    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
    )
    speaker = models.ForeignKey("speakers.Speaker", related_name="proposals")
    additional_speakers = models.ManyToManyField("speakers.Speaker", through="AdditionalSpeaker",
                                                 blank=True)
    cancelled = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    cached_tags = models.TextField(blank=True, default='', editable=False)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def can_edit(self):
        """
        Return True if this proposal is editable - meaning no presentation exists yet.
        """
        proposal_section = ProposalSection.objects.filter(section=self.kind.section).first()
        if proposal_section.is_available():
            return True
        return False

        # Putting this import at the top would result in a circular import
        from symposion.schedule.models import Presentation
        return not Presentation.objects.filter(proposal_base=self).exists()

    def cache_tags(self):
        self.cached_tags = self.get_tags_display()
        self.save()

    def get_tags_display(self):
        return u", ".join(self.tags.names())

    @property
    def section(self):
        return self.kind.section

    @property
    def speaker_email(self):
        return self.speaker.email

    @property
    def number(self):
        return str(self.pk).zfill(3)

    @property
    def status(self):
        try:
            return self.result.status
        except ObjectDoesNotExist:
            return 'undecided'

    def as_dict(self, details=False):
        """Return a dictionary representation of this proposal."""

        # Put together the base dict.
        answer = {
            'id': self.id,
            'speakers': [i.as_dict for i in self.speakers()],
            'status': self.status,
            'title': self.title,
        }

        # Include details iff they're requested.
        if details:
            answer['details'] = {
                'abstract': self.abstract,
                'description': self.description,
                'notes': self.additional_notes,
            }

            # If there is extra data that has been set, include it also.
            try:
                answer['extra'] = json.loads(self.data.data)
            except ObjectDoesNotExist:
                pass

        # Return the answer.
        return answer

    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.exclude(
                additionalspeaker__status=AdditionalSpeaker.SPEAKING_STATUS_DECLINED):
            yield speaker

    def notification_email_context(self):
        return {
            "title": self.title,
            "speaker": self.speaker.name,
            "speakers": ', '.join([x.name for x in self.speakers()]),
            "kind": self.kind.name,
        }


reversion.register(ProposalBase)


class AdditionalSpeaker(models.Model):

    SPEAKING_STATUS_PENDING = 1
    SPEAKING_STATUS_ACCEPTED = 2
    SPEAKING_STATUS_DECLINED = 3

    SPEAKING_STATUS = [
        (SPEAKING_STATUS_PENDING, _("Pending")),
        (SPEAKING_STATUS_ACCEPTED, _("Accepted")),
        (SPEAKING_STATUS_DECLINED, _("Declined")),
    ]

    speaker = models.ForeignKey("speakers.Speaker")
    proposalbase = models.ForeignKey(ProposalBase)
    status = models.IntegerField(choices=SPEAKING_STATUS, default=SPEAKING_STATUS_PENDING)

    def __unicode__(self):
        return u'Additional speaker {} for "{}"'.format(
            self.speaker, self.proposalbase)

    class Meta:
        db_table = "proposals_proposalbase_additional_speakers"
        unique_together = ("speaker", "proposalbase")


def uuid_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("document", filename)


class SupportingDocument(models.Model):

    proposal = models.ForeignKey(ProposalBase, related_name="supporting_documents")

    uploaded_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    file = models.FileField(upload_to=uuid_filename)
    description = models.CharField(max_length=140)

    def download_url(self):
        return reverse("proposal_document_download",
                       args=[self.pk, os.path.basename(self.file.name).lower()])
