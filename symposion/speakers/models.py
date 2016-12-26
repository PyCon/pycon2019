import datetime
import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_photo_path(instance, filename):
    """
    Generate the path where we save the uploaded photo.
    Store the files under speaker_photos.
    To avoid problems with non-ASCII, generate a random UUID and use that as
    the base filename, with the original filename's extension appended.
    """
    # file will be uploaded to MEDIA_ROOT/speaker_photos/<UUID>.extension
    extension = os.path.splitext(filename)[1]
    uuid = uuid4()
    return 'speaker_photos/{}{}'.format(uuid, extension)


class Speaker(models.Model):

    user = models.OneToOneField(User, null=True, related_name="speaker_profile")
    name = models.CharField(max_length=100,
                            help_text=_(u"As you would like it to appear in "
                                        u"the conference program."))
    biography = models.TextField(
        help_text=_(u"A little bit about you. 100 words or less, please. This "
                    u"will be used in print publications so please keep it "
                    u"simple, no links or formatting."))
    photo = models.ImageField(upload_to=get_photo_path, blank=True)
    twitter_username = models.CharField(
        max_length=15,
        blank=True,
        help_text=_(u"Your Twitter account")
    )
    mobile_number = models.CharField(max_length=40, blank=True)
    annotation = models.TextField()  # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True)
    invite_token = models.CharField(max_length=40, db_index=True)
    created = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        # Test self.user_id instead of self.user because referencing self.user
        # forces a query.
        if self.user_id is not None:
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
