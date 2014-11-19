from django.core.urlresolvers import reverse

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
