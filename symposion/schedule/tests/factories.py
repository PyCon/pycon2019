import datetime
import factory
import factory.fuzzy

from pycon.tests.factories import PyConTutorialProposalFactory
from symposion.conference.tests.factories import SectionFactory
from symposion.speakers.tests.factories import SpeakerFactory

from ..models import Presentation, Slot, SlotKind, Day, Schedule


class ScheduleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Schedule

    section = factory.SubFactory(SectionFactory)


class DayFactory(factory.DjangoModelFactory):
    class Meta:
        model = Day
    schedule = factory.SubFactory(ScheduleFactory)
    date = factory.fuzzy.FuzzyDate(start_date=datetime.date.today())


class SlotKindFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlotKind

    schedule = factory.SubFactory(ScheduleFactory)
    label = factory.fuzzy.FuzzyText()


class SlotFactory(factory.DjangoModelFactory):
    class Meta:
        model = Slot

    day = factory.SubFactory(DayFactory)
    # .kind and .day both need to point at the same schedule
    kind = factory.SubFactory(
        SlotKindFactory,
        schedule=factory.LazyAttribute(lambda kind: kind.factory_parent.day.schedule)
    )
    start = factory.LazyAttribute(lambda n: datetime.time())
    end = factory.LazyAttribute(lambda n: datetime.time())


class PresentationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Presentation

    title = 'Presentation'
    description = 'Description'
    abstract = 'Abstract'
    speaker = factory.SubFactory(SpeakerFactory)
    proposal_base = factory.SubFactory(PyConTutorialProposalFactory)
    section = factory.SubFactory(SectionFactory)
    slot = factory.SubFactory(SlotFactory)
