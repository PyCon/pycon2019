from django.contrib.auth import get_user_model
from django.test import TestCase

from social_auth.exceptions import AuthException

from symposion.social_auth.pipeline.user import create_user


class SocialAuthTest(TestCase):
    def test_create_user(self):
        details = {
            'email': 'user@example.com',
        }
        retval = create_user(
            backend=None,
            details=details,
            response=None,
            uid=None,
            username="john",
            user=None,
        )
        self.assertTrue(retval['is_new'])
        user = retval['user']
        self.assertTrue(isinstance(user, get_user_model()))
        self.assertEqual('user@example.com', user.email)

    def test_no_username(self):
        # returns None
        retval = create_user(
            backend=None,
            details=None,
            response=None,
            uid=None,
            username=None,
            user=None,
        )
        self.assertIsNone(retval)

    def test_user_exists(self):
        # If a user exists with the same email address, raise exception
        get_user_model().objects.create_user("john", "user@example.com")
        details = {
            'email': 'user@example.com',
        }
        with self.assertRaises(AuthException):
            create_user(
                backend=None,
                details=details,
                response=None,
                uid=None,
                username="john",
                user=None,
            )
