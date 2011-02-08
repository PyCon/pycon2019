# encoding: utf-8
import datetime

from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from biblion import creole_parser


class Track(models.Model):
    
    name = models.CharField(max_length=65)
    
    def __unicode__(self):
        return self.name


class Session(models.Model):
    
    track = models.ForeignKey(Track, null=True, related_name="sessions")


class SessionRole(models.Model):
    
    SESSION_ROLE_CHAIR = 1
    SESSION_ROLE_RUNNER = 2
    
    SESSION_ROLE_TYPES = [
        (SESSION_ROLE_CHAIR, "Session Chair"),
        (SESSION_ROLE_RUNNER, "Session Runner"),
    ]
    
    session = models.ForeignKey(Session)
    user = models.ForeignKey(User)
    role = models.IntegerField(choices=SESSION_ROLE_TYPES)
    status = models.NullBooleanField()
    
    submitted = models.DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        unique_together = [("session", "user", "role")]


# @@@ precreate the Slots with proposal == None and then making the schedule is just updating slot.proposal and/or title/notes
class Slot(models.Model):
    
    title = models.CharField(max_length=100, null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    kind = models.ForeignKey(ContentType, null=True)
    track = models.ForeignKey(Track, null=True, related_name="slots")
    session = models.ForeignKey(Session, null=True, related_name="slots")
    
    def __unicode__(self):
        return u"%s: %s — %s" % (self.start.strftime("%a"), self.start.strftime("%X"), self.end.strftime("%X"))


class Presentation(models.Model):
    
    PRESENTATION_TYPE_TALK = 1
    PRESENTATION_TYPE_PANEL = 2
    PRESENTATION_TYPE_TUTORIAL = 3
    PRESENTATION_TYPE_POSTER = 4
    
    PRESENTATION_TYPES = [
        (PRESENTATION_TYPE_TALK, "Talk"),
        (PRESENTATION_TYPE_PANEL, "Panel"),
        (PRESENTATION_TYPE_TUTORIAL, "Tutorial"),
        (PRESENTATION_TYPE_POSTER, "Poster")
    ]
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]
    
    slot = models.ForeignKey(Slot, null=True, blank=True, related_name="presentations")
    
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "Brief one paragraph blurb (will be public if accepted). Must be 400 characters or less"
    )
    presentation_type = models.IntegerField(choices=PRESENTATION_TYPES)
    abstract = models.TextField(
        help_text = "More detailed description (will be public if accepted). You can use <a href='http://wikicreole.org/' target='_blank'>creole</a> markup. <a id='preview' href='#'>Preview</a>",
    )
    abstract_html = models.TextField(editable=False)
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    
    submitted = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False,
    )
    speaker = models.ForeignKey("speakers.Speaker", related_name="sessions")
    additional_speakers = models.ManyToManyField("speakers.Speaker", blank=True)
    cancelled = models.BooleanField(default=False)
    
    extreme_pycon = models.BooleanField(u"EXTREME PyCon!", default=False)
    invited = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.abstract_html = creole_parser.parse(self.abstract)
        super(Presentation, self).save(*args, **kwargs)
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker
    
    def __unicode__(self):
        return u"%s" % self.title
