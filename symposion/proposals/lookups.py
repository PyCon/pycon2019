from django.contrib.auth.models import User

from selectable.base import ModelLookup
from selectable.registry import registry


class UserLookup(ModelLookup):
    model = User
    search_fields = (
        'first_name__icontains',
        'last_name__icontains',
        'email__icontains',
    )

    def get_item_value(self, item):
        return item.email

    def get_item_label(self, item):
        return u"%s (%s)" % (item.get_full_name(), item.email)

    def create_item(self, value):
        """We aren't actually creating a new user, we just need to supply the
           email to the form processor
        """
        return value

registry.register(UserLookup)
