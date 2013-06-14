from django.contrib.auth import get_user_model

from account.models import EmailAddress
from social_auth.exceptions import AuthException
from social_auth.utils import setting


def create_user(backend, details, response, uid, username, user=None,
                *args, **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {"user": user}
    if not username:
        return None

    if not setting("SOCIAL_AUTH_CREATE_USERS", True):
        return None

    email = details.get("email")

    if EmailAddress.objects.filter(email=email):
        # TODO - Make this fail gracefully back to sign up
        message = (
            "The email address provided by the external "
            "service is already associated with another account. Please "
            "log in to that account first and associate your account."
        )
        raise AuthException(backend, message)
    else:
        User = get_user_model()
        user = User.objects.create_user(username=username, email=email)

    return {
        "user": user,
        "is_new": True
    }
