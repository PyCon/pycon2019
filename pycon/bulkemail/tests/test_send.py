from __future__ import unicode_literals
import json
import smtplib
from django.core import mail
from django.test import TestCase
from mock import patch
from pycon.bulkemail.models import BulkEmail, SENT, ERROR


class BulkEmailSendTest(TestCase):
    def setUp(self):
        self.bulk = BulkEmail.objects.create(
            subject="My email subject",
            body="Body line 1\nBody line 2\nBody line 3\n",
            from_address="from@example.com",
            to_addresses=["to1@example.com", "to2@example.com"],
            bcc_addresses=["bcc1@example.com", "bcc2@example.com"],
            headers=json.dumps({
                'Header1': 'value1',
                'Header2': 'value2 value3',
            }),
        )
        self.assertEqual(len(mail.outbox), 0)

    def check_send(self):
        # Verify that the expected emails were sent
        # Get updated object
        bulk = BulkEmail.objects.get(pk=self.bulk.pk)
        self.assertEqual(SENT, bulk.status)

        # Should have sent one message
        self.assertEqual(len(mail.outbox), 1)

        out = mail.outbox[0]
        msg = out.message()
        self.assertEqual(self.bulk.subject, msg['Subject'])
        self.assertIn(self.bulk.body, msg.as_string())
        self.assertEqual(self.bulk.from_address, msg['From'])
        self.assertEqual(', '.join(self.bulk.to_addresses), msg['To'])
        self.assertNotIn('Bcc', msg)
        self.assertEqual('value1', msg['Header1'])
        self.assertEqual('value2 value3', msg['Header2'])
        for address in self.bulk.bcc_addresses:
            self.assertIn(address, out.recipients())

    def test_successful_send(self):
        self.bulk.send()
        self.check_send()

    def test_no_to_addresses(self):
        self.bulk.to_addresses = []
        self.bulk.save()
        self.bulk.send()
        self.check_send()

    def test_no_bcc_addresses(self):
        self.bulk.bcc_addresses = []
        self.bulk.save()
        self.bulk.send()
        self.check_send()

    # Now let's break it
    def test_no_addresses(self):
        self.bulk.to_addresses = []
        self.bulk.bcc_addresses = []
        self.bulk.save()
        self.bulk.send()
        # It should NOT have sent the message because there was nobody to send it to
        self.assertEqual(len(mail.outbox), 0)

    def test_send_failed(self):
        with patch('django.core.mail.message.EmailMessage.send') as mock_send:
            mock_send.side_effect = smtplib.SMTPException("No server")
            self.bulk.send()
        self.assertEqual(len(mail.outbox), 0)  # we mocked the actual send, so...
        bulk = BulkEmail.objects.get(pk=self.bulk.pk)
        self.assertEqual(ERROR, bulk.status)
        self.assertEqual("No server", bulk.error)

    def test_already_sent(self):
        self.bulk.status = SENT
        self.bulk.save()
        self.bulk.send()
        self.assertEqual(len(mail.outbox), 0)
        bulk = BulkEmail.objects.get(pk=self.bulk.pk)
        self.assertEqual(SENT, bulk.status)
