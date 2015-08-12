import factory
from symposion.conference.models import Section, Conference


class ConferenceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Conference


class SectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Section

    conference = factory.SubFactory(ConferenceFactory)
