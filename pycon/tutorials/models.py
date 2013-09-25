import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from pycon.models import PyConTutorialProposal

class PyConTutorialMessage(models.Model):
    """Message attached to a tutorial."""
    tutorial = models.ForeignKey(PyConTutorialProposal,
                                 related_name="tutorial_messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             help_text=_(u"User who submitted the message"))
    message = models.TextField()
    submitted_at = models.DateTimeField(default=datetime.datetime.now,
                                        editable=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __unicode__(self):
        return u"%s message submitted: %s" % (self.tutorial, self.submitted_at)

