import datetime

from django.test import TestCase
from freezegun import freeze_time

from symposion.proposals.tests.factories import (
    ProposalBaseFactory,
    ProposalKindFactory,
    ProposalSectionFactory,
)
from symposion.conference.tests.factories import SectionFactory


class ProposalsTest(TestCase):
    def test_can_edit(self):
        conf_section = SectionFactory(slug="widgets")
        prop_section = ProposalSectionFactory(section=conf_section)
        prop_kind = ProposalKindFactory(section=conf_section, slug="widget")
        prop = ProposalBaseFactory(kind=prop_kind)

        # Normal Operation
        prop_section.closed = False
        prop_section.save()
        self.assertTrue(prop.can_edit())

        # Start/End Dates

        prop_section.start = datetime.datetime(2017, 9, 20)
        prop_section.end = datetime.datetime(2017, 9, 29)
        prop_section.save()

        with freeze_time("2017-09-19"):
            self.assertFalse(prop.can_edit())

        with freeze_time("2017-09-25"):
            self.assertTrue(prop.can_edit())

        with freeze_time("2017-09-30"):
            self.assertFalse(prop.can_edit())

        # Explicit Close
        with freeze_time("2017-09-25"):
            prop_section.closed = True
            prop_section.save()
            self.assertFalse(prop.can_edit())
