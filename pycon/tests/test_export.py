from __future__ import unicode_literals

from httplib import OK
from zipfile import ZipFile
from StringIO import StringIO
from datetime import timedelta, date
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now
from pycon.sponsorship.models import SponsorLevel, Sponsor, Benefit
from pycon.tests.factories import PyConTutorialProposalFactory
from symposion.conference.models import Conference, current_conference, Section
from symposion.proposals.models import ProposalKind
from symposion.proposals.tests.factories import ProposalBaseFactory
from symposion.schedule.models import Schedule, Slot, Day, SlotKind
from symposion.schedule.tests.factories import PresentationFactory


class ProgramExportTest(TestCase):
    fixtures = [
        'fixtures/conference.json',
        'fixtures/proposal_base.json'
    ]

    def setUp(self):
        self.url = reverse('program_export')
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)
        conference = current_conference()
        self.sponsor_level = SponsorLevel.objects.create(
            conference=conference, name="Lead", cost=1)
        self.sponsor = Sponsor.objects.create(
            name="Big Daddy",
            level=self.sponsor_level,
            active=True,
        )

        # Create our benefits, of various types
        self.text_benefit = Benefit.objects.create(name="text", type="text")
        self.file_benefit = Benefit.objects.create(name="file", type="file")
        # These names must be spelled exactly this way:
        self.weblogo_benefit = Benefit.objects.create(
            name="Web logo", type="weblogo")
        self.printlogo_benefit = Benefit.objects.create(
            name="Print logo", type="file")
        self.advertisement_benefit = Benefit.objects.create(
            name="Advertisement", type="file")

        yesterday = now() - timedelta(hours=24)
        tomorrow = now() + timedelta(hours=24)

        for kind_name in ['Talk', 'Tutorial']:
            slug = kind_name.lower()
            section, __ = Section.objects.get_or_create(
                conference=conference,
                name__iexact=kind_name + "s",  # Section names are plural
                defaults=dict(name=kind_name + "s",
                              start_date=yesterday,
                              end_date=tomorrow,
                              slug=slug))
            ProposalKind.objects.get_or_create(name__iexact=kind_name, defaults=dict(slug=slug, section=section))
            Schedule.objects.get_or_create(section=section)

    def test_talks_schedule(self):
        section=Section.objects.get(name='Talks')
        schedule=Schedule.objects.get(section=section)

        day=Day.objects.create(schedule=schedule, date=date.today())
        kind=SlotKind.objects.create(schedule=schedule, label="Foo")
        slot = Slot.objects.create(
            day=day,
            kind=kind,
            start=now().time(),
            end=now().time(),
        )
        pres = PresentationFactory(
            title="Faffa the dog",
            abstract="Tinkerbell",
            description="Not very much, thank you",
            section=section,
            slot=slot,
            cancelled=False,
        )

        rsp = self.client.get(self.url)
        self.assertEqual(OK, rsp.status_code)
        self.assertEqual('attachment; filename=program_export.zip', rsp['Content-Disposition'])

        zipfile = ZipFile(StringIO(rsp.content), "r")
        # Check out the zip - testzip() returns None if no errors found
        self.assertIsNone(zipfile.testzip())

        fname = "program_export/schedule/csv/talks_schedule.csv"
        file_contents = zipfile.open(fname, "U").read().decode('utf-8')
        self.assertIn(pres.title, file_contents)
        self.assertIn(pres.abstract, file_contents)

    def test_tutorials_presentation(self):
        section=Section.objects.get(name='Tutorials')
        schedule=Schedule.objects.get(section=section)
        prop_kind = ProposalKind.objects.get(name__iexact='tutorial')
        proposal = PyConTutorialProposalFactory(
            kind=prop_kind,
            title="Faffa the dog",
            abstract="Tinkerbell",
        )
        day=Day.objects.create(schedule=schedule, date=date.today())
        kind=SlotKind.objects.create(schedule=schedule, label="Foo")
        slot = Slot.objects.create(
            day=day,
            kind=kind,
            start=now().time(),
            end=now().time(),
        )
        pres = PresentationFactory(
            title=proposal.title,
            abstract=proposal.abstract,
            description="Not very much, thank you",
            section=section,
            slot=slot,
            cancelled=False,
            proposal_base=proposal,
        )
        rsp = self.client.get(self.url)
        self.assertEqual(OK, rsp.status_code)
        self.assertEqual('attachment; filename=program_export.zip', rsp['Content-Disposition'])

        zipfile = ZipFile(StringIO(rsp.content), "r")
        # Check out the zip - testzip() returns None if no errors found
        self.assertIsNone(zipfile.testzip())

        fname = "program_export/presentations/csv/tutorials.csv"
        file_contents = zipfile.open(fname, "U").read().decode('utf-8')
        self.assertIn(pres.title, file_contents)
        self.assertIn(pres.abstract, file_contents)
