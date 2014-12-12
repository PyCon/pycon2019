from django.test import TestCase

from pycon.tests import factories

from .. import forms


class TestGroupRegistrationForm(TestCase):
    form_class = forms.GroupRegistrationForm


    def setUp(self):
        super(TestGroupRegistrationForm, self).setUp()
        self.data = {
            'first_name': 'Sam',
            'last_name': 'Green',
            'email': 'test@example.com',
        }

    def test_first_name_optional(self):
        self.data.pop('first_name')
        form = self.form_class(self.data)
        self.assertTrue(form.is_valid())

    def test_last_name_optional(self):
        self.data.pop('last_name')
        form = self.form_class(self.data)
        self.assertTrue(form.is_valid())

    def test_email_required(self):
        self.data.pop('email')
        form = self.form_class(self.data)
        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form.errors)

    def test_existing_user(self):
        existingUser = factories.UserFactory(email=self.data['email'])
        form = self.form_class(self.data)
        self.assertTrue(form.is_valid())
        created, user = form.save()
        self.assertFalse(created)
        self.assertEqual(user, existingUser)
        self.assertEqual(user.email, self.data['email'])

    def test_new_user(self):
        form = self.form_class(self.data)
        self.assertTrue(form.is_valid())
        created, user = form.save()
        self.assertTrue(created)
        self.assertEqual(user.email, self.data['email'])
        self.assertEqual(user.first_name, self.data['first_name'])
        self.assertEqual(user.last_name, self.data['last_name'])
