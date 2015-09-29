import factory
import factory.django
import factory.fuzzy

from symposion.conference.tests.factories import get_conference

from .. import models


class SponsorLevelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SponsorLevel

    conference = get_conference()
    name = factory.fuzzy.FuzzyText()
    cost = factory.fuzzy.FuzzyInteger(1, 10000)


class SponsorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Sponsor

    applicant = factory.SubFactory('pycon.tests.factories.UserFactory')
    name = factory.fuzzy.FuzzyText()
    external_url = 'http://example.com'
    contact_name = factory.fuzzy.FuzzyText()
    contact_emails = factory.Sequence(lambda n: 'sponsor-{}@example.com'.format(n))
    contact_phone = factory.fuzzy.FuzzyText()
    contact_address = factory.fuzzy.FuzzyText()
    level = factory.SubFactory('pycon.sponsorship.tests.factories.SponsorLevelFactory')
