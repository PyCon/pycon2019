from httplib import OK
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from pycon.models import SpecialEvent

from pycon.tests.factories import SpecialEventFactory
from symposion.conference.models import Conference


class ExportJSONIncludesSpecialEventsTest(TestCase):
    def setUp(self):
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)
        self.event1 = SpecialEventFactory()
        self.event2 = SpecialEventFactory()
        # unpublished events not included
        self.event3 = SpecialEventFactory(published=False)

    def test_json_export(self):
        url = reverse("schedule_json")
        rsp = self.client.get(url)
        self.assertEqual(OK, rsp.status_code)
        data = json.loads(rsp.content.decode('utf-8'))
        self.assertEqual(2, len(data))
        for item in data:
            self.assertEqual("special event", item['kind'])
            event = SpecialEvent.objects.get(slug=item['slug'], published=True)
            self.assertEqual(event.name, item['name'])
            self.assertEqual(event.description, item['description'])
            self.assertEqual(event.location, item['location'])
            self.assertEqual(event.start.isoformat(), item['start'])
            self.assertEqual(event.end.isoformat(), item['end'])
