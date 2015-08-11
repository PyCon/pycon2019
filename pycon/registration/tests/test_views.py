import json

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from account.models import Account
from django.test import override_settings

from pycon.tests import factories
from pycon.tests.base import TransactionViewTestCase, ViewTestCase

from ..views import GroupRegistration


class TestCTERegistrationLogin(ViewTestCase):
    url_name = "registration_login"

    def test_unauthenticated(self):
        """View requires authentication."""
        self.client.logout()
        response = self.client.get(reverse(self.url_name))
        self.assertRedirectsToLogin(response)

    def test_authenticated(self):
        """View requires authentication."""
        self.login_user()
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(200, response.status_code)


class GroupRegistrationTestMixin(object):
    url_name = "group_registration"

    def setUp(self):
        super(GroupRegistrationTestMixin, self).setUp()
        self.permission = Permission.objects.create(
            content_type=ContentType.objects.get_for_model(User),
            codename='group_registration',
            name="Can add group registrations",
        )
        self.user = self.create_user()
        self.user.user_permissions.add(self.permission)
        self.login_user(self.user)

    @override_settings(ACCOUNT_CREATE_ON_SAVE=False)
    def create_user(self, **kwargs):
        return factories.UserFactory(**kwargs)

    def post(self, data):
        # By default, the Django test client interprets POST data as a
        # dictionary. By using a different content type it uses the data as-is.
        return self.client.post(reverse(self.url_name), data=data,
                                content_type="application/x-www-form-urlencoded")

    def get_created_users(self):
        return User.objects.exclude(pk=self.user.pk)


class TestGroupRegistration(GroupRegistrationTestMixin, ViewTestCase):
    """See also transaction-related tests below."""

    def test_unauthenticated(self):
        """User must have group registration permission."""
        self.client.logout()
        for method_name in ('get', 'post'):
            method = getattr(self.client, method_name)
            response = method(reverse(self.url_name))
            self.assertRedirectsToLogin(response)

    def test_no_permission(self):
        """User must have group registration permission."""
        self.user.user_permissions.all().delete()
        for method_name in ('get', 'post'):
            method = getattr(self.client, method_name)
            response = method(reverse(self.url_name))
            self.assertRedirectsToLogin(response)

    def test_valid_get(self):
        """Page should render if user has group registration permission."""
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_post_not_json(self):
        """400 response should be returned if invalid JSON is posted."""
        data = "["  # not JSON-encoded
        response = self.post(data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(GroupRegistration.format_error in response.content)

    def test_post_not_list(self):
        """400 response should be returned if JSON is not a list of dicts."""
        data = json.dumps("not a list")
        response = self.post(data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(GroupRegistration.format_error in response.content)

    def test_post_not_list_of_dicts(self):
        """400 response should be returned if JSON is not a list of dicts."""
        data = json.dumps(["asdf"])
        response = self.post(data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(GroupRegistration.format_error in response.content)

    def test_post_no_registrations(self):
        """Case of no registrations."""
        data = json.dumps([])
        response = self.post(data)
        self.assertEqual(response.status_code, 200)

        users = self.get_created_users()
        self.assertFalse(users.exists())
        self.assertFalse(Account.objects.exists())

        user_data = json.loads(response.content)
        self.assertTrue(user_data['success'])
        self.assertEqual(user_data['users'], [])

    def test_one_valid_registration(self):
        """Case of one valid registration."""
        data = json.dumps([
            {'first_name': 'Sam', 'last_name': 'Green', 'email': 'x@test.com'},
        ])
        response = self.post(data)
        self.assertEqual(response.status_code, 200)

        users = self.get_created_users()
        self.assertEqual(users.count(), 1)
        user = users.get(email='x@test.com', first_name='Sam', last_name='Green')
        self.assertEqual(Account.objects.filter(user=user).count(), 1)

        user_data = json.loads(response.content)
        self.assertTrue(user_data['success'])

        self.assertEqual(len(user_data['users']), 1)
        self.assertDictEqual(user_data['users'][0], {
            'valid': True,
            'created': True,
            'user': {
                'pycon_id': user.pk,
                'first_name': 'Sam',
                'last_name': 'Green',
                'email': 'x@test.com',
            },
        })

    def test_multiple_valid_registrations(self):
        """Case of multiple valid registrations."""
        data = json.dumps([
            {'first_name': 'Sam', 'last_name': 'Green', 'email': 'x@test.com'},
            {'first_name': 'Alex', 'last_name': 'Blue', 'email': 'y@test.com'},
        ])
        response = self.post(data)
        self.assertEqual(response.status_code, 200)

        users = self.get_created_users()
        self.assertEqual(users.count(), 2)
        user1 = users.get(email='x@test.com', first_name='Sam', last_name='Green')
        self.assertEqual(Account.objects.filter(user=user1).count(), 1)
        user2 = users.get(email='y@test.com', first_name='Alex', last_name='Blue')
        self.assertEqual(Account.objects.filter(user=user2).count(), 1)

        user_data = json.loads(response.content)
        self.assertTrue(user_data['success'])

        self.assertEqual(len(user_data['users']), 2)
        self.assertDictEqual(user_data['users'][0], {
            'valid': True,
            'created': True,
            'user': {
                'pycon_id': user1.pk,
                'first_name': 'Sam',
                'last_name': 'Green',
                'email': 'x@test.com',
            },
        })
        self.assertDictEqual(user_data['users'][1], {
            'valid': True,
            'created': True,
            'user': {
                'pycon_id': user2.pk,
                'first_name': 'Alex',
                'last_name': 'Blue',
                'email': 'y@test.com',
            },
        })

    def test_already_registered(self):
        """User should be retrieved rather than created if email exists."""
        existing_user = self.create_user(
            first_name='Already', last_name='Here', email='x@test.com')
        data = json.dumps([
            {'first_name': 'Sam', 'last_name': 'Green', 'email': 'x@test.com'},
        ])
        response = self.post(data)
        self.assertEqual(response.status_code, 200)

        users = self.get_created_users()
        self.assertEqual(users.count(), 1)
        user = users.get(
            first_name='Already', last_name='Here', email='x@test.com',
            pk=existing_user.pk)
        self.assertFalse(Account.objects.filter(user=user).exists())

        user_data = json.loads(response.content)
        self.assertTrue(user_data['success'])

        self.assertEqual(len(user_data['users']), 1)
        self.assertDictEqual(user_data['users'][0], {
            'valid': True,
            'created': False,
            'user': {
                'pycon_id': user.pk,
                'first_name': 'Sam',
                'last_name': 'Green',
                'email': 'x@test.com',
            },
        })

    def test_name_not_required(self):
        """First name and last name are not required."""
        data = json.dumps([
            {'email': 'x@test.com'},
        ])
        response = self.post(data)
        self.assertEqual(response.status_code, 200)

        users = self.get_created_users()
        self.assertEqual(users.count(), 1)
        user = users.get(email='x@test.com', first_name='', last_name='')
        self.assertEqual(Account.objects.filter(user=user).count(), 1)

        user_data = json.loads(response.content)
        self.assertTrue(user_data['success'])

        self.assertEqual(len(user_data['users']), 1)
        self.assertDictEqual(user_data['users'][0], {
            'valid': True,
            'created': True,
            'user': {
                'pycon_id': user.pk,
                'first_name': '',
                'last_name': '',
                'email': 'x@test.com',
            },
        })

    def test_one_invalid_registration(self):
        """No user should be created if any registration data is invalid."""
        data = json.dumps([
            {'first_name': 'asdf', 'last_name': 'asdf'},
        ])
        response = self.post(data)
        self.assertEqual(response.status_code, 200)

        users = self.get_created_users()
        self.assertFalse(users.exists())
        self.assertFalse(Account.objects.exists())

        user_data = json.loads(response.content)
        self.assertFalse(user_data['success'])

        self.assertEqual(len(user_data['users']), 1)
        self.assertFalse(user_data['users'][0]['valid'])
        self.assertIsNone(user_data['users'][0]['user'])
        self.assertTrue('errors' in user_data['users'][0])
        self.assertEqual(len(user_data['users'][0]['errors']), 1)

    def test_multiple_invalid_registrations(self):
        """No user should be created if any registration data is invalid."""
        data = json.dumps([
            {'first_name': 'asdf', 'last_name': 'asdf'},
            {'first_name': 'asdf', 'last_name': 'asdf', 'email': 'invalid'},
        ])
        response = self.post(data)
        self.assertEqual(response.status_code, 200)

        users = self.get_created_users()
        self.assertFalse(users.exists())
        self.assertFalse(Account.objects.exists())

        user_data = json.loads(response.content)
        self.assertFalse(user_data['success'])

        self.assertEqual(len(user_data['users']), 2)
        self.assertFalse(user_data['users'][0]['valid'])
        self.assertIsNone(user_data['users'][0]['user'])
        self.assertTrue('errors' in user_data['users'][0])
        self.assertEqual(len(user_data['users'][0]['errors']), 1)
        self.assertFalse(user_data['users'][1]['valid'])
        self.assertIsNone(user_data['users'][1]['user'])
        self.assertTrue('errors' in user_data['users'][1])
        self.assertEqual(len(user_data['users'][1]['errors']), 1)


class TestGroupRegistrationTransactions(GroupRegistrationTestMixin,
                                        TransactionViewTestCase):
    """
    Group registration tests that require transaction management via
    TransactionTestCase.

    Separated from the tests above for speed.
    """

    def test_mixed_validity_registrations(self):
        """No user should be created if any registration data is invalid."""
        data = json.dumps([
            {'email': 'valid@example.com'},
            {'email': 'invalid'},
        ])
        response = self.post(data)
        self.assertEqual(response.status_code, 200)

        users = self.get_created_users()
        self.assertFalse(users.exists())
        self.assertFalse(Account.objects.exists())

        user_data = json.loads(response.content)
        self.assertFalse(user_data['success'])

        self.assertEqual(len(user_data['users']), 2)
        self.assertTrue(user_data['users'][0]['valid'])
        self.assertIsNone(user_data['users'][0]['user'])
        self.assertFalse('errors' in user_data['users'][0])
        self.assertFalse(user_data['users'][1]['valid'])
        self.assertIsNone(user_data['users'][1]['user'])
        self.assertTrue('errors' in user_data['users'][1])
        self.assertEqual(len(user_data['users'][1]['errors']), 1)
