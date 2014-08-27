import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from ..models import FinancialAidApplication, FinancialAidMessage
from pycon.finaid.forms import FinancialAidApplicationForm, ReviewerMessageForm


today = datetime.date.today()


class FinancialAidTest(TestCase):

    def test_form(self):
        user = User.objects.create_user("Foo")
        instance = FinancialAidApplication(user=user)
        form = FinancialAidApplicationForm(instance=instance)
        self.assertFalse(form.is_valid())
        data = dict(
            profession="Foo",
            experience_level="lots",
            what_you_want="money",
            use_of_python="fun",
            presenting=1,
            travel_amount_requested="0.00",
        )
        instance = FinancialAidApplication(user=user)
        form = FinancialAidApplicationForm(data, instance=instance)
        self.assertTrue(form.is_valid(), msg=form.errors)

        # Leave out a required field
        del data['presenting']
        form = FinancialAidApplicationForm(data, instance=instance)
        self.assertFalse(form.is_valid())

    def test_reviewer_message_form(self):
        user = User.objects.create_user("Foo")
        application = FinancialAidApplication.objects.create(
            user=user,
            profession="Foo",
            experience_level="lots",
            what_you_want="money",
            use_of_python="fun",
            presenting=1,
        )
        application.save()
        message = FinancialAidMessage(user=user, application=application)
        data = {
            'visible': False,
            'message': 'TestMessage'
        }
        form = ReviewerMessageForm(data, instance=message)
        self.assertTrue(form.is_valid())
        message = form.save()
        message = FinancialAidMessage.objects.get(pk=message.pk)
        self.assertFalse(message.visible)
        self.assertEqual("TestMessage", message.message)

        data['visible'] = True
        form = ReviewerMessageForm(data, instance=message)
        self.assertTrue(form.is_valid())
        message = form.save()
        message = FinancialAidMessage.objects.get(pk=message.pk)
        self.assertTrue(message.visible)
