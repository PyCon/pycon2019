import factory.django

from pycon.bulkemail.models import BulkEmail


class BulkEmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BulkEmail
