import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from ..models import FinancialAidApplication


today = datetime.date.today()


class TestFinancialAidModels(TestCase):
    def test_one(self):
        """Can create the application object"""
        FinancialAidApplication()

    def test_reverse_relation(self):
        user = User.objects.create_user("Foo")
        with self.assertRaises(FinancialAidApplication.DoesNotExist):
            getattr(user, 'financial_aid')

        # Just the minimum required fields
        x = FinancialAidApplication.objects.create(
            user=user,
            profession="Foo",
            experience_level="lots",
            what_you_want="money",
            want_to_learn="stuff",
            use_of_python="fun",
            presenting=1,
        )
        # the reverse relation works
        self.assertEqual(x, user.financial_aid)
