import factory
from symposion.conference.tests.factories import SectionFactory
from symposion.proposals.models import ProposalKind, ProposalBase, ProposalSection
from symposion.speakers.tests.factories import SpeakerFactory


class ProposalKindFactory(factory.DjangoModelFactory):
    class Meta:
        model = ProposalKind
        django_get_or_create = ('slug',)

    section = factory.SubFactory(SectionFactory)


class ProposalBaseFactory(factory.DjangoModelFactory):
    class Meta:
        model = ProposalBase

    speaker = factory.SubFactory(SpeakerFactory)


class ProposalSectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = ProposalSection
