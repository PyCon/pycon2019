import random

import factory
import factory.django
import factory.fuzzy

from django.contrib.auth import models as auth

from pycon.models import PyConProposalCategory, PyConProposal, \
    PyConTalkProposal, PyConTutorialProposal, ThunderdomeGroup, PyConLightningTalkProposal

from symposion.proposals.tests.factories import ProposalKindFactory, \
    ProposalBaseFactory
from symposion.reviews.models import ProposalResult


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = auth.User

    username = factory.fuzzy.FuzzyText()
    first_name = factory.fuzzy.FuzzyText()
    last_name = factory.fuzzy.FuzzyText()
    email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))


class ProposalResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProposalResult


class PyConProposalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PyConProposalCategory


class PyConProposalFactory(ProposalBaseFactory):
    class Meta:
        model = PyConProposal
        abstract = True

    category = factory.SubFactory(PyConProposalCategoryFactory)
    audience_level = factory.LazyAttribute(lambda a: random.choice([1, 2, 3]))


class PyConTalkProposalFactory(PyConProposalFactory):
    class Meta:
        model = PyConTalkProposal

    duration = 0

    kind = factory.SubFactory(ProposalKindFactory,
                              name="talk",
                              slug="talk")
    outline = "outline"
    audience = "audience"
    perceived_value = "perceived_value"


class PyConTutorialProposalFactory(PyConProposalFactory):
    class Meta:
        model = PyConTutorialProposal

    kind = factory.SubFactory(ProposalKindFactory,
                              name="tutorial",
                              slug="tutorial")

    domain_level = 1
    outline = "outline"
    more_info = "more info"
    audience = "audience"
    perceived_value = "perceived_value"


class ThunderdomeGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ThunderdomeGroup


class PyConLightningTalkProposalFactory(PyConProposalFactory):
    class Meta:
        model = PyConLightningTalkProposal

    kind = factory.SubFactory(ProposalKindFactory,
                              name="lightning",
                              slug="lightning")
