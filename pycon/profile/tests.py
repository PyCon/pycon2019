from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from pycon.profile.models import Profile
from symposion.conference.models import Conference


class TestProfileViews(TestCase):
    url = reverse('profile_edit')
    username = "user@example.com"
    first_name = "Sam"
    last_name = "McGillicuddy"

    def setUp(self):
        self.user = User.objects.create_user(self.username,
                                             password="pass",
                                             email=self.username)
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()
        assert self.client.login(username=self.username, password="pass")
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)

    def test_profile_view_get(self):
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        # Profile should have been created
        Profile.objects.get(user=self.user)
        assert rsp.context['form']

    def test_profile_view_post(self):
        data = {
            'user': self.user.id,
            'first_name': 'Joe',
            'last_name': "O'Reilly",
            'phone': '1-234-567-8901',
        }
        rsp = self.client.post(self.url, data)
        # NB: view does not redirect after post, unless there was a 'next'
        # in the GET parameters, which can hardly happen when we're posting.
        self.assertEqual(200, rsp.status_code)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual('Joe', profile.first_name)


class TestProfile(TestCase):
    username = "user@example.com"
    first_name = "Sam"
    last_name = "McGillicuddy"

    def setUp(self):
        self.user = User.objects.create_user(self.username,
                                             password="pass",
                                             email=self.username)
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()

    def test_is_complete(self):
        # A Profile object is complete if all fields are non-block,
        # except maybe the 'phone'
        p = Profile(id=1, user=self.user,
                    first_name='ralph', last_name='cramden')
        self.assertTrue(p.is_complete)
        p.first_name = ''
        self.assertFalse(p.is_complete)
        p.phone = '123'
        self.assertFalse(p.is_complete)
        p.first_name = 'ralph'
        self.assertTrue(p.is_complete)

    def test_display_name(self):
        p = Profile(id=1, user=self.user,
                    first_name='ralph', last_name='cramden')
        self.assertEqual("ralph cramden", p.display_name)
