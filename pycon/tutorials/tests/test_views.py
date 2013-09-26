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

    def test_post_email_attendee(self):
        # redirect to send email form
        self.presentation.proposal.registrants.add(self.user)
        self.login()
        data = {
            'email_action': '',
        }
        rsp = self.client.post(self.tutorial_url, data)
        self.assertEqual(302, rsp.status_code)
        self.assertIn(self.tutorial_url, rsp['Location'])

    def test_post_email_speaker(self):
        # redirect to tutorial, missing email selections
        speaker = SpeakerFactory(user=self.user)
        self.presentation.speaker = speaker
        self.presentation.save()
        self.login()
        data = {
            'email_action': '',
            'user_1': 1
        }
        msg_url = reverse('tutorial_email',kwargs={
                                            'pk': self.presentation.proposal.pk,
                                            'pks': self.user.pk
                                            })
        rsp = self.client.post(self.tutorial_url, data)
        self.assertEqual(302, rsp.status_code)
        self.assertIn(msg_url, rsp['Location'])



# class TestFinaidEmailView(TestCase, TestMixin, ReviewTestMixin):
#     def setUp(self):
#         self.user = self.create_user()
#         self.make_reviewer(self.user)
#         self.login()
#         self.application = create_application(user=self.user)
#         self.application.save()
#         self.url = reverse('finaid_email', kwargs={'pks': self.application.pk})
#         # Create 2nd user and application, just to make sure we're only
#         # using the ones that were asked for and not all of them.
#         self.user2 = self.create_user(username="jill",
#                                       email="jill@example.com")
#         self.application2 = create_application(user=self.user2)
#         self.application2.save()

#     def test_email_view(self):
#         # Just look at the email view, check the context
#         rsp = self.client.get(self.url)
#         if rsp.status_code == 302:
#             self.fail(rsp['Location'])
#         self.assertEqual(200, rsp.status_code)
#         context = rsp.context
#         self.assertEqual([self.user], context['users'])

#     @patch('django.template.Template.render')
#     @patch('pycon.finaid.views.send_mass_mail')
#     def test_email_submit(self, mock_send_mass_mail, mock_render):
#         # Actually submit the thing

#         # Create review record
#         # Most fields are optional
#         data = {
#             'application': self.application,
#             'status': STATUS_SUBMITTED,
#             'hotel_amount': Decimal('6.66'),
#             'registration_amount': Decimal('0.00'),
#             'travel_amount': Decimal('0.00'),
#         }
#         review = FinancialAidReviewData(**data)
#         review.save()

#         subject = 'TEST SUBJECT'
#         template_text = 'THE TEMPLATE'
#         FinancialAidEmailTemplate.objects.create(
#             name='template',
#             template="wrong template"
#         )
#         template2 = FinancialAidEmailTemplate.objects.create(
#             name='template',
#             template=template_text,
#         )
#         data = {
#             'template': template2.pk,
#             'subject': subject,
#         }
#         mock_render.return_value = template_text
#         rsp = self.client.post(self.url, data)
#         self.assertEqual(302, rsp.status_code, rsp.content)
#         # we tried to send the right emails
#         expected_msgs = [(subject, template_text, email_address(),
#                           [self.user.email])]
#         mock_send_mass_mail.assert_called_with(expected_msgs)
#         # the template was rendered with a good context
#         context = mock_render.call_args[0][0]
#         self.assertEqual(self.application, context['application'])
#         self.assertEqual(review, context['review'])


class TestTutorialMessageView(TestCase, TestMixin):
    def setUp(self):
        self.presentation = PresentationFactory()
        self.tutorial_url = reverse('schedule_presentation_detail', args=[self.presentation.pk])
        self.user = self.create_user()


    def test_messaging(self):
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
