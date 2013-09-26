from django.contrib.auth.models import User
from django.test import TestCase

from pycon.tests.factories import PyConTutorialProposalFactory

from ..forms import BulkEmailForm, TutorialMessageForm
from ..models import PyConTutorialMessage

class TutorialFormsTest(TestCase):

    def test_message_form(self):
        user = User.objects.create_user("Foo")
        tutorial = PyConTutorialProposalFactory.create()
        instance = PyConTutorialMessage(tutorial=tutorial, user=user)
        form = TutorialMessageForm(instance=instance)
        self.assertFalse(form.is_valid())
        data = dict(
            message="A Message!",
        )
        instance = PyConTutorialMessage(tutorial=tutorial, user=user)
        form = TutorialMessageForm(data, instance=instance)
        self.assertTrue(form.is_valid(), msg=form.errors)

        # Leave out a required field
        del data['message']
        form = TutorialMessageForm(data, instance=instance)
        self.assertFalse(form.is_valid())


    def test_bulk_email_form(self):
        data = {
            'subject': 'Test Subject',
            'body': 'Test Body'
        }
        form = BulkEmailForm(data)
        self.assertTrue(form.is_valid())

        # leave out a required field
        del data['subject']
        form = BulkEmailForm(data)
        self.assertFalse(form.is_valid())
