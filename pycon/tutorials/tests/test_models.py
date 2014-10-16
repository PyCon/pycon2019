from django.contrib.auth.models import User
from django.test import TestCase

from pycon.tests.factories import PyConTutorialProposalFactory

from ..models import PyConTutorialMessage


class PyConTutorialMessageModelTest(TestCase):
    def test_one(self):
        """Can create the application object"""
        PyConTutorialMessage()

    def test_reverse_relation(self):
        user = User.objects.create_user("Foo")
        tutorial = PyConTutorialProposalFactory.create()
        self.assertFalse(tutorial.tutorial_messages.all())

        # Just the minimum required fields
        x = PyConTutorialMessage.objects.create(
            tutorial=tutorial,
            user=user,
            message="Foo",
        )
        # the reverse relation works
        self.assertEqual(x, tutorial.tutorial_messages.all()[0])
