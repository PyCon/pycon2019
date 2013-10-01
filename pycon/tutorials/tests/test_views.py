from mock import patch

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from pycon.finaid.tests.utils import TestMixin
from symposion.schedule.tests.factories import PresentationFactory
from symposion.speakers.tests.factories import SpeakerFactory

from ..models import PyConTutorialMessage


class TestTutorialSchedulePresentationView(TestMixin, TestCase):
    """ Tests for Schedule Presentation Detail view with enhancements for Tutorials """

    def setUp(self):
        self.presentation = PresentationFactory()
        self.tutorial_url = reverse('schedule_presentation_detail', args=[self.presentation.pk])
        self.user = self.create_user()

    def test_no_messaging(self):
        # Ensure Messages widgets are not in the content if not an attendee
        rsp = self.client.get(self.tutorial_url)
        self.assertNotIn('id="messages"', rsp.content)
        self.login()
        rsp = self.client.get(self.tutorial_url)
        self.assertNotIn('id="messages"', rsp.content)

    def test_attendee(self):
        # If an attendee, messaging avaialable
        self.presentation.proposal.registrants.add(self.user)
        self.login()
        rsp = self.client.get(self.tutorial_url)
        self.assertIn('id="messages"', rsp.content)

    def test_speaker(self):
        # Avaialable to speakers
        speaker = SpeakerFactory(user=self.user)
        self.presentation.speaker = speaker
        self.presentation.save()
        self.login()
        rsp = self.client.get(self.tutorial_url)
        self.assertIn('id="messages"', rsp.content)

    def test_cospeaker(self):
        # Avaialable to cospeakers
        speaker = SpeakerFactory(user=self.user)
        self.presentation.additional_speakers.add(speaker)
        self.login()
        rsp = self.client.get(self.tutorial_url)
        self.assertIn('id="messages"', rsp.content)

    def test_is_staff(self):
        # Avaialable to staff
        self.user.is_staff = True
        self.user.save()
        self.login()
        rsp = self.client.get(self.tutorial_url)
        self.assertIn('id="messages"', rsp.content)

    def test_post_message(self):
        # redirect to send message form
        self.presentation.proposal.registrants.add(self.user)
        self.login()
        data = {
            'message_action': '',
        }
        msg_url = reverse('tutorial_message', kwargs={'pk': self.presentation.proposal.pk})
        rsp = self.client.post(self.tutorial_url, data)
        self.assertEqual(302, rsp.status_code)
        self.assertIn(msg_url, rsp['Location'])

    def test_post_email_from_attendee(self):
        # validation error
        self.presentation.proposal.registrants.add(self.user)
        self.login()
        data = {
            'email_action': '',
        }
        rsp = self.client.post(self.tutorial_url, data)
        self.assertEqual(302, rsp.status_code)
        self.assertIn(self.tutorial_url, rsp['Location'])

    def test_post_email_from_speaker(self):
        # redirect to send email form, ,
        speaker = SpeakerFactory(user=self.user)
        self.presentation.speaker = speaker
        self.presentation.save()
        self.login()
        data = {
            'email_action': '',
            'user_1': 1
        }
        email_url = reverse('tutorial_email', kwargs={
                                                'pk': self.presentation.pk,
                                                'pks': 1
                                            })
        rsp = self.client.post(self.tutorial_url, data)
        self.assertEqual(302, rsp.status_code)
        self.assertIn(email_url, rsp['Location'])


class TestTutorialEmailView(TestCase, TestMixin):
    def setUp(self):
        self.presentation = PresentationFactory()
        self.tutorial_url = reverse('schedule_presentation_detail', args=[self.presentation.pk])
        self.user = self.create_user()

    @patch('pycon.tutorials.views.send_email_message')
    def test_email_submit_as_attendee(self, mock_send_mail):
        speaker = SpeakerFactory(user=self.create_user('speaker', 'speaker@conf.com'))
        self.presentation.speaker = speaker
        self.presentation.save()
        self.presentation.proposal.registrants.add(self.user)
        self.login()
        # Actually submit the thing
        data = {
            'subject': 'Test Subject',
            'body': 'Test Body'
        }
       # We can display the page prompting for a message to send them
        url = reverse('tutorial_email',kwargs={
                                            'pk': self.presentation.pk,
                                            'pks': self.presentation.speaker.user.pk
                                            })
        rsp = self.client.post(url, data)
        self.assertEqual(302, rsp.status_code, rsp.content)
        self.assertEqual(1, mock_send_mail.call_count)
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(kwargs['bcc'][0], [self.presentation.speaker.user.email][0])

    @patch('pycon.tutorials.views.send_email_message')
    def test_email_submit_as_speaker(self, mock_send_mail):
        attendee = self.create_user(username='foo', email="foo@bar.com")
        speaker = SpeakerFactory(user=self.user)
        self.presentation.speaker = speaker
        self.presentation.save()
        self.login()
        # Actually submit the thing
        data = {
            'subject': 'Test Subject',
            'body': 'Test Body'
        }
       # We can display the page prompting for a message to send them
        url = reverse('tutorial_email',kwargs={
                                            'pk': self.presentation.pk,
                                            'pks': attendee.pk
                                            })
        rsp = self.client.post(url, data)
        self.assertEqual(302, rsp.status_code, rsp.content)
        self.assertEqual(1, mock_send_mail.call_count)
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(kwargs['bcc'][0], [attendee.email][0])


class TestTutorialMessageView(TestCase, TestMixin):
    def setUp(self):
        self.presentation = PresentationFactory()
        self.tutorial_url = reverse('schedule_presentation_detail', args=[self.presentation.pk])
        self.user = self.create_user()

    def test_messaging_as_attendee(self):
        self.presentation.proposal.registrants.add(self.user)
        self.login()
        rsp = self.client.get(self.tutorial_url)
        self.assertIn('id="messages"', rsp.content)

       # We can display the page prompting for a message to send them
        url = reverse('tutorial_message', kwargs={'pk': self.presentation.proposal.pk})
        rsp = self.client.get(url)
        self.assertEqual(200, rsp.status_code)

        # "Send" a message to those two applications
        test_message = 'One if by land and two if by sea'
        data = {'message': test_message, }
        rsp = self.client.post(url, data=data)
        self.assertEqual(302, rsp.status_code)
        msg = PyConTutorialMessage.objects.get(user=self.user, tutorial=self.presentation.proposal)
        self.assertEqual(test_message, msg.message)

        # For each message, it's visible, so it should have been emailed to
        # both the other attendees and speakers. Total: 1 message for this case
        self.assertEqual(1, len(mail.outbox))

    def test_messaging_as_speaker(self):
        speaker = SpeakerFactory(user=self.user)
        self.presentation.speaker = speaker
        self.presentation.save()
        self.login()
        rsp = self.client.get(self.tutorial_url)
        self.assertIn('id="messages"', rsp.content)

       # We can display the page prompting for a message to send them
        url = reverse('tutorial_message', kwargs={'pk': self.presentation.proposal.pk})
        rsp = self.client.get(url)
        self.assertEqual(200, rsp.status_code)

        # "Send" a message to those two applications
        test_message = 'One if by land and two if by sea'
        data = {'message': test_message, }
        rsp = self.client.post(url, data=data)
        self.assertEqual(302, rsp.status_code)
        msg = PyConTutorialMessage.objects.get(user=self.user, tutorial=self.presentation.proposal)
        self.assertEqual(test_message, msg.message)

        # For each message, it's visible, so it should have been emailed to
        # both the other attendees and speakers. Total: 1 message for this case
        self.assertEqual(1, len(mail.outbox))
