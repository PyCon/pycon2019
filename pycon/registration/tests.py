from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestRegistration(TestCase):
    def test_cte_login_view_login_required(self):
        # cte_login_view requires login
        url = reverse('registration_login')
        rsp = self.client.get(url)
        login_url = reverse("account_login")
        self.assertRedirects(rsp, login_url + "?next=" + url)

    def test_cte_login_view_works(self):
        # cte_login_view renders a page okay if we're logged in
        url = reverse('registration_login')
        username = "user@example.com"
        User.objects.create_user(username, password="pass",
                                 email=username)
        assert self.client.login(username=username, password="pass")
        rsp = self.client.get(url)
        self.assertEqual(200, rsp.status_code)
