import factory
from symposion.conference.tests.factories import SectionFactory
from symposion.proposals.models import ProposalKind, ProposalBase
from symposion.speakers.tests.factories import SpeakerFactory


class ProposalKindFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProposalKind
    FACTORY_DJANGO_GET_OR_CREATE = ('slug',)

    section = factory.SubFactory(SectionFactory)


class ProposalBaseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProposalBase
    ABSTRACT_FACTORY = True

    speaker = factory.SubFactory(SpeakerFactory)
