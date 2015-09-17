from httplib import OK, NOT_FOUND

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.dateformat import format, time_format

from pycon.finaid.tests.utils import TestMixin
from pycon.models import EduSummitTalkProposal, PyConTalkProposal, PyConProposal
from pycon.tests.factories import SpecialEventFactory, PyConProposalCategoryFactory, \
    PyConEduSummitProposalFactory, PyConLightningTalkProposalFactory, PyConTalkProposalFactory
from symposion.conference.models import Conference, current_conference
from symposion.conference.tests.factories import SectionFactory
from symposion.proposals.kinds import get_proposal_model
from symposion.proposals.models import ProposalKind
from symposion.proposals.tests.factories import ProposalSectionFactory
from symposion.reviews.models import Review
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
        section = SectionFactory(conference=current_conference(), slug='edusummits')
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


class ChangeStatusProposal(TestMixin, TestCase):

    def check_one_kind(self, kind_slug, factory):
        section_slug = kind_slug + "s"
        speaker = SpeakerFactory(user=self.create_user())
        section = SectionFactory(conference=current_conference(), slug=section_slug)
        ProposalSectionFactory(section=section)
        kind, __ = ProposalKind.objects.get_or_create(slug=kind_slug, section=section)
        proposal = factory(
            kind=kind,
            speaker=speaker,
        )

        # Create a new user to be the reviewer, because nobody
        # can review their own proposals.
        reviewer = self.create_user(username="reviewer", email="reviewer@example.com")
        ct = ContentType.objects.get_for_model(Review)
        perm, __ = Permission.objects.get_or_create(
            codename="can_review_%s" % section_slug,
            name="Can review %s proposals" % kind_slug,
            content_type=ct)
        reviewer.user_permissions.add(perm)
        perm, __ = Permission.objects.get_or_create(
            codename="can_manage_%s" % section_slug,
            name="Can manage %s proposals" % kind_slug,
            content_type=ct)
        reviewer.user_permissions.add(perm)
        self.login(username="reviewer")

        url = reverse('review_section', args=(section_slug,))
        data = {
            'status': PyConProposal.STATUS_REJECTED,
            'pk': proposal.pk
        }
        rsp = self.client.post(url, data, follow=False)
        self.assertRedirects(rsp, url)
        model = get_proposal_model(kind_slug)
        assert model
        prop = model.objects.get(pk=proposal.pk)
        self.assertEqual(PyConProposal.STATUS_REJECTED, prop.overall_status)

    def test_edusummit(self):
        self.check_one_kind(kind_slug='edusummit', factory=PyConEduSummitProposalFactory)

    def test_lightning(self):
        self.check_one_kind(kind_slug='lightning-talk', factory=PyConLightningTalkProposalFactory)

    def test_talk(self):
        self.check_one_kind(kind_slug='talk', factory=PyConTalkProposalFactory)
