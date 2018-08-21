import os.path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from pycon.tests.factories import UserFactory

from .. import forms

from .factories import SponsorLevelFactory

# Tiny image file for testing
TEST_IMAGE_FILENAME = os.path.join(os.path.dirname(__file__), 'colormap.png')
TEST_IMAGE = open(TEST_IMAGE_FILENAME, "rb").read()


class TestSponsorApplicationForm(TestCase):
    form_class = forms.SponsorApplicationForm

    def setUp(self):
        super(TestSponsorApplicationForm, self).setUp()
        self.sponsor_level = SponsorLevelFactory()
        self.user = UserFactory()
        self.second_email = 'foo@example.com'
        self.data = {
            'name': 'Sponsor',
            'contact_name': self.user.get_full_name(),
            'contact_emails': self.user.email + "\n" + self.second_email,
            'contact_phone': '336-867-5309',
            'contact_address': '123 Main Street, Anytown, NC 90210',
            'level': self.sponsor_level.pk,
            'wants_table': True,
            'wants_booth': True,
            'external_url': 'https://example.com',
            'web_description': 'Funky sponsor',
        }
        self.files = {
            'web_logo': SimpleUploadedFile('file.png', TEST_IMAGE),
        }

    def test_initial(self):
        """User data should be passed in as initial data."""
        form = self.form_class(user=self.user)
        self.assertEqual(form.initial['contact_name'],
                         self.user.get_full_name())
        self.assertEqual(form.initial['contact_emails'], [self.user.email])

    def test_user_saved_as_applicant(self):
        """User should be saved as the sponsor's applicant."""
        form = self.form_class(user=self.user, data=self.data, files=self.files)
        sponsor = form.save()
        self.assertEqual(sponsor.applicant, self.user)
        self.assertEqual(sponsor.contact_emails, [self.user.email, self.second_email])

    def validate_field_required(self, field_name, value=None, error=None):
        # Test that a field is required, or some value is not valid.
        # If value is None, don't supply that field; otherwise, use that value
        # Expect the field name to be in the errors.
        # If 'error' given, expect that to be form.errors[field_name]
        if value is None:
            self.data.pop(field_name)
        else:
            self.data[field_name] = value
        form = self.form_class(user=self.user, data=self.data, files=self.files)
        self.assertFalse(form.is_valid())
        self.assertIn(field_name, form.errors)
        if error:
            self.assertEqual(error, form.errors[field_name])

    def test_contact_email_required(self):
        """Must be at least one contact email"""
        self.validate_field_required('contact_emails', '', [u'This field is required.'])

    def test_contact_emails_validated(self):
        self.validate_field_required('contact_emails', 'not_an_email\nfoo@example.com',
                                     [u'Enter valid email addresses.'])

    def test_phone_required(self):
        """Contact phone number is a required field."""
        self.validate_field_required('contact_phone')

    def test_address_required(self):
        """Contact address is a required field."""
        self.validate_field_required('contact_address')

    def test_wants_booth_optional(self):
        """
        wants_booth is optional and should be stored as False if not given.
        """
        self.data.pop('wants_booth')
        form = self.form_class(user=self.user, data=self.data, files=self.files)
        self.assertTrue(form.is_valid(), msg=form.errors)
        sponsor = form.save()
        self.assertFalse(sponsor.wants_booth)

    def test_wants_booth_true(self):
        form = self.form_class(user=self.user, data=self.data, files=self.files)
        self.assertTrue(form.is_valid(), msg=form.errors)
        sponsor = form.save()
        self.assertTrue(sponsor.wants_booth)

    def test_wants_table_optional(self):
        """
        wants_table is optional and should be stored as False if not given.
        """
        self.data.pop('wants_table')
        form = self.form_class(user=self.user, data=self.data, files=self.files)
        self.assertTrue(form.is_valid(), msg=form.errors)
        sponsor = form.save()
        self.assertFalse(sponsor.wants_table)

    def test_wants_table_true(self):
        form = self.form_class(user=self.user, data=self.data, files=self.files)
        self.assertTrue(form.is_valid(), msg=form.errors)
        sponsor = form.save()
        self.assertTrue(sponsor.wants_table)

    def test_company_link_required(self):
        self.validate_field_required('external_url')

    def test_company_description_required(self):
        self.validate_field_required('web_description')

    def test_web_logo_required(self):
        self.files.pop('web_logo')
        form = self.form_class(user=self.user, data=self.data, files=self.files)
        self.assertFalse(form.is_valid())
        self.assertIn('web_logo', form.errors)
