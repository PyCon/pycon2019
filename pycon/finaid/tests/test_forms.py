from django.contrib.auth.models import User
from django.test import TestCase

from ..models import FinancialAidApplication
from pycon.finaid.forms import FinancialAidApplicationForm


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
            want_to_learn="stuff",
            use_of_python="fun",
            presenting=1,
            hotel_nights=0,
            travel_amount_requested="0.00",
        )
        instance = FinancialAidApplication(user=user)
        form = FinancialAidApplicationForm(data, instance=instance)
        self.assertTrue(form.is_valid(), msg=form.errors)

        # Leave out a required field
        del data['presenting']
        form = FinancialAidApplicationForm(data, instance=instance)
        self.assertFalse(form.is_valid())
