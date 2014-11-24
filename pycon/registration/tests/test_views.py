from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from pycon.tests import factories
from pycon.tests.base import ViewTestCase


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


class TestGroupRegistration(ViewTestCase):
    url_name = "group_registration"

    def setUp(self):
        super(TestGroupRegistration, self).setUp()
        self.permission = Permission.objects.create(
            content_type=ContentType.objects.get_for_model(User),
            codename='group_registration',
            name="Can add group registrations",
        )
        self.user = factories.UserFactory()
        self.user.user_permissions.add(self.permission)
        self.login_user(self.user)

    def test_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse(self.url_name))
        self.assertRedirectsToLogin(response)

    def test_no_permission(self):
        self.user.user_permissions.all().delete()
        response = self.client.get(reverse(self.url_name))
        self.assertRedirectsToLogin(response)

    def test_get(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
