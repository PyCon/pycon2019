from httplib import OK, NOT_FOUND

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.dateformat import format, time_format
from pycon.finaid.tests.utils import TestMixin
from pycon.models import EduSummitTalkProposal, PyConTalkProposal

from pycon.tests.factories import SpecialEventFactory, PyConProposalCategoryFactory
from symposion.conference.models import Conference, current_conference
from symposion.conference.tests.factories import SectionFactory
from symposion.proposals.models import ProposalKind
from symposion.proposals.tests.factories import ProposalSectionFactory
from symposion.speakers.tests.factories import SpeakerFactory


def format_datetime(dt):
    return format(dt, settings.DATE_FORMAT) + ", " + time_format(dt, settings.TIME_FORMAT)


class SpecialEventViewTest(TestCase):
    def setUp(self):
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)
        self.event = SpecialEventFactory()

    def test_view_event(self):
        rsp = self.client.get(self.event.get_absolute_url())
        self.assertEqual(OK, rsp.status_code)
        self.assertContains(rsp, self.event.name)
        self.assertContains(rsp, self.event.location)
        self.assertContains(rsp, self.event.description)

        self.assertContains(rsp, format_datetime(self.event.start))
        self.assertContains(rsp, format_datetime(self.event.end))

    def test_cant_view_unpublished_event(self):
        self.event.published = False
        self.event.save()
        rsp = self.client.get(self.event.get_absolute_url())
        self.assertEqual(NOT_FOUND, rsp.status_code)


class CreateEduSummitProposal(TestMixin, TestCase):
    def test_create_edusummit_proposal(self):
        SpeakerFactory(user=self.create_user())
        self.login()
        section = SectionFactory(conference=current_conference(), slug='edusummit')
        ProposalSectionFactory(section=section)
        ProposalKind.objects.get_or_create(slug='edusummit', section=section)

        url = reverse('proposal_submit_kind', args=['edusummit'])
        data = {
            'category': PyConProposalCategoryFactory().pk,
            'audience_level': PyConTalkProposal.AUDIENCE_LEVEL_NOVICE,
            'description': 'Rad',
            'title': 'Massively rad',
        }
        self.assertFalse(EduSummitTalkProposal.objects.exists())
        rsp = self.client.post(url, data)
        self.assertRedirects(rsp, reverse('dashboard'))
        # There should now be one
        prop = EduSummitTalkProposal.objects.get()
        self.assertEqual(data['description'], prop.description)
        self.assertEqual(data['title'], prop.title)
