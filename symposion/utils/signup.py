import hashlib
import random

from django.contrib.auth.models import User


def generate_username(email):
    def random_username():
        h = hashlib.sha1(email).hexdigest()[:25]
        # don't ask
        n = random.randint(1, (10 ** (5 - 1)) - 1)
        return "%s%d" % (h, n)
    while True:
        try:
            username = random_username()
            User.objects.get(username=username)
        except User.DoesNotExist:
            break
    return username
