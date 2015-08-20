from __future__ import unicode_literals
import logging
import json

from django.core.mail.message import EmailMessage
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from multi_email_field.fields import MultiEmailField


logger = logging.getLogger(__name__)
UNSENT, INPROGRESS, SENT, ERROR = range(4)


class BulkEmail(models.Model):
    """
    Track a bulk email that needs to be sent in the background

    Important: By default, the MIME type of the body parameter in an
    EmailMessage is "text/plain". That makes it safe to use "|safe" in
    our email templates, and we do. If you change this to, say, send
    HTML format email, you must go through the email templates and do
    something better about escaping user data for safety.
    """
    status = models.IntegerField(
        choices=[
            (UNSENT, "Unsent"),
            (INPROGRESS, "In progress"),
            (SENT, "Sent"),
            (ERROR, "Error"),
        ],
        default=UNSENT
    )

    subject = models.CharField(max_length=250)
    body = models.TextField()
    from_address = models.EmailField()
    to_addresses = MultiEmailField(default=[])
    bcc_addresses = MultiEmailField(default=[])
    headers = models.TextField()  # stored as JSON
    error = models.TextField(default='', blank=True)

    start_time = models.DateTimeField(
        null=True, blank=True, default=None,
        help_text=_("Time when we started trying to send. Used to detect orphan records.")
    )
    end_time = models.DateTimeField(
        null=True, blank=True, default=None,
        help_text=_("When we finished trying to send.")
    )

    def get_context(self):
        return json.loads(self.context)

    def get_headers(self):
        return json.loads(self.headers)

    def send(self):
        """Send the message"""
        # Make sure this BulkEmail is neither sent nor in progress already,
        # and atomically set it to INPROGRESS so only one thread can be trying
        # to send it.
        num_updates = BulkEmail.objects.filter(pk=self.pk, status=UNSENT) \
            .update(status=INPROGRESS, start_time=now(), end_time=None)
        if 1 != num_updates:
            logger.info("BulkEmail %d state was %s, not UNSENT in send task, not sending.",
                        self.pk, self.get_status_display())
            return
        # Now status is INPROGRESS.  Get to work.
        try:
            email = EmailMessage(
                self.subject.rstrip(u"\n"),
                self.body,
                self.from_address,
                self.to_addresses,
                self.bcc_addresses,
                headers=self.get_headers(),
            )
            email.send()
            BulkEmail.objects.filter(pk=self.pk, status=INPROGRESS)\
                .update(status=SENT, end_time=now())
        except Exception as err:
            logger.exception("Exception sending BulkEmail")
            BulkEmail.objects.filter(pk=self.pk, status=INPROGRESS)\
                .update(status=ERROR, error=str(err), end_time=now())
        finally:
            # If we've not managed to send the email, set status to ERROR
            BulkEmail.objects.filter(pk=self.pk, status=INPROGRESS)\
                .update(status=ERROR, end_time=now())
