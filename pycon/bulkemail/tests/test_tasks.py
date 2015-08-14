from mock import patch

from django.test import TestCase
from django.utils.timezone import now

from pycon.bulkemail.models import INPROGRESS, BulkEmail, UNSENT, ERROR, SENT
from pycon.bulkemail.tasks import send_bulk_emails, MAX_TIME, RETRY_INTERVAL
from pycon.bulkemail.tests.factories import BulkEmailFactory


@patch('pycon.bulkemail.models.BulkEmail.send')
class BulkEmailSendTaskTest(TestCase):
    def test_nothing_to_send(self, mock_send):
        # Should just return
        send_bulk_emails()
        self.assertEqual(0, mock_send.call_count)

    def test_long_inprogress_emails(self, mock_send):
        # If an email has been INPROGRESS too long, the task
        # should change it to UNSENT so we can do something
        # with it.
        bulk = BulkEmailFactory(status=INPROGRESS, start_time=now() - 2 * MAX_TIME)
        BulkEmailFactory(status=INPROGRESS, start_time=now())  # Should not retry (yet)
        send_bulk_emails()
        self.assertEqual(1, mock_send.call_count)
        bulk2 = BulkEmail.objects.get(pk=bulk.pk)
        self.assertEqual(UNSENT, bulk2.status)
        self.assertEqual(1, mock_send.call_count)

    def test_retry_error_emails(self, mock_send):
        # After long enough, retry errored emails
        BulkEmailFactory(status=ERROR, end_time=now())  # Should not retry (yet)
        bulk = BulkEmailFactory(status=ERROR, end_time=now() - 2 * RETRY_INTERVAL)
        send_bulk_emails()
        self.assertEqual(1, mock_send.call_count)
        bulk2 = BulkEmail.objects.get(pk=bulk.pk)
        self.assertEqual(UNSENT, bulk2.status)
        self.assertEqual(1, mock_send.call_count)

    def test_call_send(self, mock_send):
        # Make multiple BulkEmails, but we should only call send on
        # the one with the UNSENT status.
        BulkEmailFactory(status=UNSENT)
        BulkEmailFactory(status=ERROR)
        BulkEmailFactory(status=SENT)
        BulkEmailFactory(status=INPROGRESS)
        send_bulk_emails()
        self.assertEqual(1, mock_send.call_count)

    def test_call_exceptions(self, mock_send):
        # If sending raises exceptions, we still keep going
        BulkEmailFactory(status=UNSENT)
        BulkEmailFactory(status=UNSENT)
        mock_send.side_effect = Exception("Intentional exception during testing")
        send_bulk_emails()
        self.assertEqual(2, mock_send.call_count)
