from django.test import TestCase

from pycon.tests.factories import UserFactory

from .. import forms

from .factories import SponsorLevelFactory


class TestSponsorApplicationForm(TestCase):
    form_class = forms.SponsorApplicationForm

    def setUp(self):
        super(TestSponsorApplicationForm, self).setUp()
        self.sponsor_level = SponsorLevelFactory()
        self.user = UserFactory()
        self.data = {
            'name': 'Sponsor',
            'contact_name': self.user.get_full_name(),
            'contact_email': self.user.email,
            'contact_phone': '336-867-5309',
            'contact_address': '123 Main Street, Anytown, NC 90210',
            'level': self.sponsor_level.pk,
            'wants_table': True,
            'wants_booth': True,
        }

    def test_initial(self):
        """User data should be passed in as initial data."""
        form = self.form_class(user=self.user)
        self.assertEqual(form.initial['contact_name'],
                         self.user.get_full_name())
        self.assertEqual(form.initial['contact_email'], self.user.email)

    def test_user_saved_as_applicant(self):
        """User should be saved as the sponsor's applicant."""
        form = self.form_class(user=self.user, data=self.data)
        sponsor = form.save()
        self.assertEqual(sponsor.applicant, self.user)

    def test_phone_required(self):
        """Contact phone number is a required field."""
        self.data.pop('contact_phone')
        form = self.form_class(user=self.user, data=self.data)
        self.assertFalse(form.is_valid())
        self.assertTrue('contact_phone' in form.errors)

    def test_address_required(self):
        """Contact address is a required field."""
        self.data.pop('contact_address')
        form = self.form_class(user=self.user, data=self.data)
        self.assertFalse(form.is_valid())
        self.assertTrue('contact_address' in form.errors)

    def test_wants_booth_optional(self):
        """
        wants_booth is optional and should be stored as False if not given.
        """
        self.data.pop('wants_booth')
        form = self.form_class(user=self.user, data=self.data)
        self.assertTrue(form.is_valid())
        sponsor = form.save()
        self.assertFalse(sponsor.wants_booth)

    def test_wants_booth_true(self):
        form = self.form_class(user=self.user, data=self.data)
        self.assertTrue(form.is_valid())
        sponsor = form.save()
        self.assertTrue(sponsor.wants_booth)

    def test_wants_table_optional(self):
        """
        wants_table is optional and should be stored as False if not given.
        """
        self.data.pop('wants_table')
        form = self.form_class(user=self.user, data=self.data)
        self.assertTrue(form.is_valid())
        sponsor = form.save()
        self.assertFalse(sponsor.wants_table)

    def test_wants_table_true(self):
        form = self.form_class(user=self.user, data=self.data)
        self.assertTrue(form.is_valid())
        sponsor = form.save()
        self.assertTrue(sponsor.wants_table)
