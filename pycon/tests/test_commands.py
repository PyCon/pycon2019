from random import randint

from mock import Mock, patch

from requests.exceptions import HTTPError

from account.models import EmailAddress

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from symposion.schedule.tests.factories import PresentationFactory

from pycon.models import PyConTutorialProposal
from pycon.tests.factories import PyConTutorialProposalFactory


class MockGet(Mock):

    @property
    def content(self):
        headers = '"Item","Tutorial Name","Max Attendees","User Email","PyCon ID"\n'
        row1 = '"Z01A","Tutorial %s - Wed/AM","8","john@doe.com",%s\n' % (self.tut1, self.u1)
        row2 = '"Z01A","Tutorial %s - Wed/AM","8","jane@doe.com",%s\n' % (self.tut1, self.u2)
        row3 = '"Z01B","Tutorial %s - Wed/PM","10","john@doe.com",%s' % (self.tut2, self.u1)
        return headers + row1 + row2 + row3

    def raise_for_status(self):
        return None


@patch('requests.get')
class UpdateTutorialRegistrantsTestCase(TestCase):

    def test_bad_url(self, mock_get):
        """Ensure a bad URL raises an exception."""
        mock_get.return_value = MockGet()
        with patch('pycon.tests.test_commands.MockGet.raise_for_status') as mock_404:
            mock_404.side_effect = HTTPError
            with self.assertRaises(HTTPError):
                call_command('update_tutorial_registrants')

    def test_no_matching_tutorials(self, mock_get):
        """Simple Test Case where no matches occur."""
        mock_get.return_value = MockGet(tut1=randint(1000, 1100),
                                        tut2=randint(2000, 2100))
        call_command('update_tutorial_registrants')

    def test_matching_tutorials(self, mock_get):
        """Simple Test Case where matches occur."""
        user_model = get_user_model()

        u1 = user_model.objects.create_user('john', email='john@doe.com', password='1234')
        u2 = user_model.objects.create_user('jane', email='jane@doe.com', password='1234')

        tut1 = PyConTutorialProposalFactory(title='Tutorial1')
        PresentationFactory(proposal_base=tut1)
        tut2 = PyConTutorialProposalFactory(title='Tutorial2')
        PresentationFactory(proposal_base=tut2)

        for tut in [tut1, tut2]:
            self.assertIsNone(tut.max_attendees)
            self.assertEqual(0, tut.registrants.all().count())

        mock_get.return_value = MockGet(tut1=tut1.pk,
                                        tut2=tut2.pk,
                                        u1=u1.pk,
                                        u2=u2.pk)
        call_command('update_tutorial_registrants')

        tut1 = PyConTutorialProposal.objects.get(pk=tut1.pk)
        self.assertEqual(8, tut1.max_attendees)
        self.assertEqual(2, tut1.registrants.all().count())
        for u in [u1, u2]:
            self.assertIn(u, tut1.registrants.all())

        tut2 = PyConTutorialProposal.objects.get(pk=tut2.pk)
        self.assertEqual(10, tut2.max_attendees)
        self.assertEqual(1, tut2.registrants.all().count())
        self.assertIn(u1, tut2.registrants.all())

    def test_matching_tutorials_unregister(self, mock_get):
        """Simple Test Case where matches occur and a User has unregistered"""
        user_model = get_user_model()
        u1 = user_model.objects.create_user('john', email='john@doe.com', password='1234')
        u2 = user_model.objects.create_user('jane', email='jane@doe.com', password='1234')

        tut1 = PyConTutorialProposalFactory(title='Tutorial1')
        PresentationFactory(proposal_base=tut1)
        tut2 = PyConTutorialProposalFactory(title='Tutorial2')
        PresentationFactory(proposal_base=tut2)

        # Add u2 to tut2
        tut2.registrants.add(u2)
        self.assertIsNone(tut1.max_attendees)
        self.assertIn(u2, tut2.registrants.all())

        mock_get.return_value = MockGet(tut1=tut1.pk,
                                        tut2=tut2.pk,
                                        u1=u1.pk,
                                        u2=u2.pk)
        call_command('update_tutorial_registrants')

        tut1 = PyConTutorialProposal.objects.get(pk=tut1.pk)
        self.assertEqual(8, tut1.max_attendees)
        self.assertEqual(2, tut1.registrants.all().count())
        for u in [u1, u2]:
            self.assertIn(u, tut1.registrants.all())

        tut2 = PyConTutorialProposal.objects.get(pk=tut2.pk)
        self.assertEqual(10, tut2.max_attendees)
        # updated; dropping u2 and adding u1
        self.assertEqual(1, tut2.registrants.all().count())
        self.assertIn(u1, tut2.registrants.all())

    def test_surprise_email_address(self, mock_get):
        """Simple Test Case where registrant has a different email than our DB"""
        user_model = get_user_model()
        u1 = user_model.objects.create_user('john', email='John@doe.com', password='1234')
        u2 = user_model.objects.create_user('jane', email='jane.doe@gmail.com', password='1234')

        tut1 = PyConTutorialProposalFactory(title='Tutorial1')
        PresentationFactory(proposal_base=tut1)
        tut2 = PyConTutorialProposalFactory(title='Tutorial2')
        PresentationFactory(proposal_base=tut2)

        # Add u2 to tut2
        tut2.registrants.add(u2)
        self.assertIsNone(tut1.max_attendees)
        self.assertIn(u2, tut2.registrants.all())

        mock_get.return_value = MockGet(tut1=tut1.pk,
                                        tut2=tut2.pk,
                                        u1=u1.pk,
                                        u2=u2.pk)
        call_command('update_tutorial_registrants')

        tut1 = PyConTutorialProposal.objects.get(pk=tut1.pk)
        self.assertEqual(8, tut1.max_attendees)
        self.assertEqual(2, tut1.registrants.all().count())
        for u in [u1, u2]:
            self.assertIn(u, tut1.registrants.all())

        tut2 = PyConTutorialProposal.objects.get(pk=tut2.pk)
        self.assertEqual(10, tut2.max_attendees)
        # updated; dropping u2 and adding u1
        self.assertEqual(1, tut2.registrants.all().count())
        self.assertIn(u1, tut2.registrants.all())

        emails1 = EmailAddress.objects.filter(user=u1)
        emails2 = EmailAddress.objects.filter(user=u2)

        self.assertEqual(['John@doe.com'], [e.email for e in emails1])
        self.assertEqual(
            sorted(['jane@doe.com', 'jane.doe@gmail.com']),
            sorted([e.email for e in emails2])
        )
