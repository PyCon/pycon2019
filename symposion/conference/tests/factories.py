from django.conf import settings
import factory
import factory.fuzzy

from symposion.conference.models import Section, Conference


def get_conference():
    conference, _ = Conference.objects.get_or_create(id=settings.CONFERENCE_ID)
    return conference


class SectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Section
        django_get_or_create = ('slug', 'conference')

    conference = get_conference()
    slug = factory.fuzzy.FuzzyText()
