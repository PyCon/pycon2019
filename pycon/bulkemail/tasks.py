from datetime import timedelta
import logging

from celery import shared_task

from django.utils.timezone import now

from pycon.bulkemail.models import BulkEmail, UNSENT, ERROR, INPROGRESS


logger = logging.getLogger(__name__)


# Wait this long before retrying
RETRY_INTERVAL = timedelta(hours=4)

# Wait this long before concluding we somehow left an email
# abandoned in INPROGRESS state
MAX_TIME = timedelta(hours=4)


@shared_task
def send_bulk_emails():

    # If any INPROGRESS email has been that way too long, change it back to
    # UNSENT to try again.
    BulkEmail.objects.filter(status=INPROGRESS, start_time__lt=now() - MAX_TIME)\
        .update(status=UNSENT)

    # If it's past the retry time for any sends that errored previously,
    # change them back to UNSENT so we'll try again.
    BulkEmail.objects.filter(status=ERROR, end_time__lt=now() - RETRY_INTERVAL)\
        .update(status=UNSENT)

    # Try to send any unsent ones
    for bulk_email in BulkEmail.objects.filter(status=UNSENT):
        try:
            bulk_email.send()
        except Exception:
            # Catch all exceptions so we can continue trying to send other emails,
            # and one bad one doesn't block everything behind it.
            logger.exception("Unexpected exception sending bulk email")
