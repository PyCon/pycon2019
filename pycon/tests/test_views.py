from httplib import OK, NOT_FOUND

from django.conf import settings
from django.test import TestCase
from django.utils.dateformat import format, time_format

from pycon.tests.factories import SpecialEventFactory
from symposion.conference.models import Conference


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
