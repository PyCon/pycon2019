# encoding: utf-8
import datetime

from django.db import models

from biblion import creole_parser


class Event(models.Model):
    
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __unicode__(self):
        return u"%s" % self.name


# @@@ precreate the Slots with proposal == None and then making the schedule is just updating slot.proposal and/or title/notes
class Slot(models.Model):
    
    event = models.ForeignKey(Event)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    title = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return u"(%s) %s: %s — %s" % (self.event, self.start.strftime("%a"), self.start.strftime("%X"), self.end.strftime("%X"))

    def sessions(self):
        return self.session_set.all().order_by("track")


class Session(models.Model):
    
    SESSION_TYPE_TALK = 1
    SESSION_TYPE_PANEL = 2
    SESSION_TYPE_TUTORIAL = 3
    SESSION_TYPE_POSTER = 4
    
    SESSION_TYPES = [
        (SESSION_TYPE_TALK, "Talk"),
        (SESSION_TYPE_PANEL, "Panel"),
        (SESSION_TYPE_TUTORIAL, "Tutorial"),
        (SESSION_TYPE_POSTER, "Poster")
    ]
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]
    
    slot = models.ForeignKey(Slot, null=True)
    track = models.CharField(max_length=10, null=True, blank=True)
    plenary = models.BooleanField(default=False)
    
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "Brief one paragraph blurb (will be public if accepted). Must be 400 characters or less"
    )
    session_type = models.IntegerField(choices=SESSION_TYPES)
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
        super(Session, self).save(*args, **kwargs)
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker

    def __unicode__(self):
        return u"%s" % self.title
