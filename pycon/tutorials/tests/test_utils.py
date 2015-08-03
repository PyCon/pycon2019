"""Test for the tutorials.utils package"""

import datetime
import unittest

from mock import patch

from django.template import Template

from pycon.bulkemail.models import BulkEmail

from ..utils import send_email_message


today = datetime.date.today()


class TestSendEmailMessage(unittest.TestCase):
    @patch('django.core.mail.message.EmailMessage.send')
    @patch('pycon.tutorials.utils.get_template')
    def test_send_email_message(self, get_template, send_mail):
        # send_email_message comes up with the expected template names
        # and calls send_mail with the expected arguments
        test_template = Template("test template")
        get_template.return_value = test_template

        context = {'a': 1, 'b': 2}
        send_email_message("TESTNAME", "from_address", ["1", "2"], [], context)

        args, kwargs = get_template.call_args_list[0]
        expected_template_name = "tutorials/email/TESTNAME/subject.txt"
        self.assertEqual(expected_template_name, args[0])

        args, kwargs = get_template.call_args_list[1]
        expected_template_name = "tutorials/email/TESTNAME/body.txt"
        self.assertEqual(expected_template_name, args[0])

        # Creates a BulkEmail object
        self.assertEqual(1, BulkEmail.objects.count())
