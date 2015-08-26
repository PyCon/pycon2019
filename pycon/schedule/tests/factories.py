import factory
import factory.django

from pycon.schedule.models import Session, SessionRole
from symposion.schedule.tests.factories import DayFactory


class SessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Session

    day = factory.SubFactory(DayFactory)


class SessionRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SessionRole
