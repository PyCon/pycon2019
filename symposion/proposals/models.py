import datetime
import os
import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete, pre_save
from django.utils.translation import ugettext_lazy as _

import json
import reversion

from model_utils.managers import InheritanceManager
from taggit.managers import TaggableManager
from taggit.models import TaggedItem

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
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class ProposalBase(models.Model):

    objects = InheritanceManager()

    kind = models.ForeignKey(ProposalKind)

    title = models.CharField(max_length=100)
    description = models.TextField(
        _("Description"),
        max_length=400,  # @@@ need to enforce 400 in UI
        help_text="If your talk is accepted this will be made public and printed in the program. Should be one paragraph, maximum 400 characters."
    )
    abstract = models.TextField(
        _("Detailed Abstract"),
        help_text=_("Detailed description. Will be made public "
                    "if your talk is accepted.")
    )
    additional_notes = models.TextField(
        blank=True,
        help_text=_("Anything else you'd like the program committee to know "
                    "when making their selection: your past speaking "
                    "experience, open source community experience, etc.")
    )
    submitted = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
    )
    speaker = models.ForeignKey("speakers.Speaker", related_name="proposals")
    additional_speakers = models.ManyToManyField("speakers.Speaker", through="AdditionalSpeaker", blank=True)
    cancelled = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    cached_tags = models.TextField(blank=True, default='')

    def __unicode__(self):
        return self.title

    def can_edit(self):
        if hasattr(self, "presentation") and self.presentation_id:
            return False
        else:
            return True

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
        for speaker in self.additional_speakers.exclude(additionalspeaker__status=AdditionalSpeaker.SPEAKING_STATUS_DECLINED):
            yield speaker

    def notification_email_context(self):
        return {
            "title": self.title,
            "speaker": self.speaker.name,
            "speakers": ', '.join([x.name for x in self.speakers()]),
            "kind": self.kind.name,
        }


# Use signals to update our cached tags whenever taggeditems
# that refer to proposals get updated.  Basically we want to
# figure out which proposal or proposals are affected and call
# .cache_tags() on them.
def tagitem_presave(sender, instance, raw, **kwargs):
    """
    We just use the presave to notice if the save is going to
    change which proposal is linked to, and remember that for
    later.
    """
    if not raw and instance.pk:
        # TagItem already existed, might have pointed at a different record
        proposal_ct = ContentType.objects.get_for_model(ProposalBase)
        if instance.content_type_id == proposal_ct.id:
            pre_save_tagitem = sender.objects.get(pk=instance.pk)
            if pre_save_tagitem.object_id != instance.object_id:
                instance.pre_save_object_id = pre_save_tagitem.object_id
pre_save.connect(tagitem_presave, sender=TaggedItem)


def tagitem_saved(sender, instance, raw, created, using, update_fields, **kwargs):
    """
    When a tagitem linked to a proposal changes, update the proposal
    it links to.  Also update the proposal it linked to before, if different.
    """
    if not raw:
        proposal_ct = ContentType.objects.get_for_model(ProposalBase)
        if instance.content_type_id == proposal_ct.id:
            ProposalBase.objects.get(id=instance.object_id).cache_tags()
            if hasattr(instance, 'pre_save_object_id'):
                # If it pointed elsewhere before the save, update that one too
                ProposalBase.objects.get(id=instance.pre_save_object_id).cache_tags()
post_save.connect(tagitem_saved, sender=TaggedItem)


def tagitem_deleted(sender, instance, **kwargs):
    """
    When a tagitem linked to a proposal is deleted, update the proposal
    it links to.
    """
    proposal_ct = ContentType.objects.get_for_model(ProposalBase)
    if instance.content_type_id == proposal_ct.id:
        ProposalBase.objects.get(id=instance.object_id).cache_tags()
post_delete.connect(tagitem_deleted, sender=TaggedItem)


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
        return reverse("proposal_document_download", args=[self.pk, os.path.basename(self.file.name).lower()])
