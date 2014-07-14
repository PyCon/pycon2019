import factory
import factory.django
import factory.fuzzy

from .. import models


class SponsorLevelFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.SponsorLevel

    conference = factory.SubFactory(
        'symposion.conference.tests.factories.ConferenceFactory')
    name = factory.fuzzy.FuzzyText()
    cost = factory.fuzzy.FuzzyInteger(1, 10000)
