from django.contrib.auth.models import User
from django.test import TestCase

from ..models import FinancialAidApplication


class TestFinancialAidModels(TestCase):
    def test_one(self):
        """Can create the application object"""
        x = FinancialAidApplication()

    def test_reverse_relation(self):
        user = User.objects.create_user("Foo")
        with self.assertRaises(FinancialAidApplication.DoesNotExist):
            unused = user.financial_aid

        # Just the minimum required fields
        FinancialAidApplication.objects.create(
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
