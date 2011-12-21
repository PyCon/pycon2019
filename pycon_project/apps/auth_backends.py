from django.conf import settings

from django.core.validators import email_re

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class MixedAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        lookup_params = {}
        username = credentials.get("username")
        if email_re.search(username):
            name, identity = "email", credentials.get("username")
        else:
            name, identity = "username", credentials.get("username")
        if identity is None:
            return None
        lookup_params[name] = identity
        try:
            user = User.objects.get(**lookup_params)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(credentials["password"]):
                return user
    
    def has_perm(self, user, perm):
        # @@@ allow all users to add wiki pages
        wakawaka_perms = [
            "wakawaka.add_wikipage",
            "wakawaka.add_revision",
            "wakawaka.change_wikipage",
            "wakawaka.change_revision"
        ]
        if perm in wakawaka_perms and user.groups.filter(name="wiki-editors").exists():
            return True
        return super(MixedAuthenticationBackend, self).has_perm(user, perm)
