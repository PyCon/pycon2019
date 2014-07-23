import random

import factory
import factory.django
import factory.fuzzy

from django.contrib.auth import models as auth

from pycon.models import PyConProposalCategory, PyConProposal, \
    PyConTalkProposal, PyConTutorialProposal

from symposion.proposals.tests.factories import ProposalKindFactory, \
    ProposalBaseFactory


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = auth.User

    username = factory.fuzzy.FuzzyText()
    first_name = factory.fuzzy.FuzzyText()
    last_name = factory.fuzzy.FuzzyText()
    email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))


class PyConProposalCategoryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = PyConProposalCategory


class PyConProposalFactory(ProposalBaseFactory):
    FACTORY_FOR = PyConProposal
    ABSTRACT_FACTORY = True

    category = factory.SubFactory(PyConProposalCategoryFactory)
    audience_level = factory.LazyAttribute(lambda a: random.choice([1, 2, 3]))


class PyConTalkProposalFactory(PyConProposalFactory):
    FACTORY_FOR = PyConTalkProposal

    duration = 0

    kind = factory.SubFactory(ProposalKindFactory,
                              name="talk",
                              slug="talk")
    outline = "outline"
    audience = "audience"
    perceived_value = "perceived_value"


class PyConTutorialProposalFactory(PyConProposalFactory):
    FACTORY_FOR = PyConTutorialProposal

    kind = factory.SubFactory(ProposalKindFactory,
                              name="tutorial",
                              slug="tutorial")

    domain_level = 1
    outline = "outline"
    more_info = "more info"
    audience = "audience"
    perceived_value = "perceived_value"
