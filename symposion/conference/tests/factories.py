import factory
from symposion.conference.models import Section, Conference


class ConferenceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Conference


class SectionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Section

    conference = factory.SubFactory(ConferenceFactory)
