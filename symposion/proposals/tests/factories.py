import factory
import factory.fuzzy

from symposion.conference.models import Section, current_conference
from symposion.conference.tests.factories import SectionFactory
from symposion.proposals.kinds import get_kind_slugs
from symposion.proposals.models import ProposalKind, ProposalBase, ProposalSection
from symposion.speakers.tests.factories import SpeakerFactory


class ProposalKindFactory(factory.DjangoModelFactory):
    class Meta:
        model = ProposalKind
        django_get_or_create = ('slug',)

    slug = factory.fuzzy.FuzzyText()
    section = factory.SubFactory(
        SectionFactory,
        slug=factory.LazyAttribute(lambda section: section.factory_parent.slug + "s")
    )


class ProposalBaseFactory(factory.DjangoModelFactory):
    class Meta:
        model = ProposalBase

    speaker = factory.SubFactory(SpeakerFactory)


class ProposalSectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = ProposalSection


def init_kinds():
    """
    Make sure there are valid ProposalKinds and Sections for the current conference.
    """
    conference = current_conference()
    for kind_slug in get_kind_slugs():
        section_slug = kind_slug + "s"
        section, __ = Section.objects.get_or_create(
            slug=section_slug,
            conference=conference,
            defaults=dict(
                name=section_slug.capitalize(),
            )
        )
        ProposalKind.objects.get_or_create(
            slug=kind_slug,
            defaults=dict(
                section=section,
                name=kind_slug.capitalize(),
            )
        )
