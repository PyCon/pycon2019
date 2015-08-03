import factory
import factory.django
import factory.fuzzy
from pycon.bulkemail.models import BulkEmail


class BulkEmailFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = BulkEmail
