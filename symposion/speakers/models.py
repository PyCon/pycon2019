import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Speaker(models.Model):

    SESSION_COUNT_CHOICES = [
        (1, _(u"One")),
        (2, _(u"Two"))
    ]

    user = models.OneToOneField(User, null=True, related_name="speaker_profile")
    name = models.CharField(max_length=100,
                            help_text=_(u"As you would like it to appear in "
                                        u"the conference program."))
    biography = models.TextField(
        help_text=_(u"A little bit about you. 100 words or less, please. This "
                    u"will be used in print publications so please keep it "
                    u"simple, no links or formatting."))
    photo = models.ImageField(upload_to="speaker_photos", blank=True)
    twitter_username = models.CharField(
        max_length = 15,
        blank = True,
        help_text=_(u"Your Twitter account")
    )
    annotation = models.TextField() # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True)
    invite_token = models.CharField(max_length=40, db_index=True)
    created = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False
    )
    sessions_preference = models.IntegerField(
        choices=SESSION_COUNT_CHOICES,
        null=True,
        blank=True,
        help_text=_(u"If you've submitted multiple talk proposals, please let "
                    u"us know if you only want to give one or if you'd like "
                    u"to give two talks.  For tutorials and posters, state "
                    u"similar preferences in the additional notes section of "
                    u"your proposals.")
    )

    def __unicode__(self):
        if self.user:
            return self.name
        else:
            return u"?"

    def get_absolute_url(self):
        return reverse("speaker_edit")

    @property
    def as_dict(self):
        return {
            'name': self.name,
            'email': self.email,
        }

    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email

    @property
    def all_presentations(self):
        presentations = []
        if self.presentations:
            for p in self.presentations.all():
                presentations.append(p)
            for p in self.copresentations.all():
                presentations.append(p)
        return presentations
