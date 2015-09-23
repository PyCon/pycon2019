import factory
import factory.fuzzy

from symposion.conference.models import Section, Conference


class ConferenceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Conference


class SectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Section
        django_get_or_create = ('slug', 'conference')

    conference = factory.SubFactory(ConferenceFactory)
    slug = factory.fuzzy.FuzzyText()
