from __future__ import unicode_literals
import datetime
from httplib import OK, FORBIDDEN
import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from pycon.pycon_api.models import APIAuth
from pycon.pycon_api.tests import RawDataClientMixin
from pycon.schedule.models import SessionRole
from pycon.schedule.tests.factories import SessionFactory, SessionRoleFactory
from pycon.tests.factories import UserFactory
from symposion.schedule.tests.factories import SlotFactory


class SessionStaffJSONTest(RawDataClientMixin, TestCase):
    def setUp(self):
        super(SessionStaffJSONTest, self).setUp()
        self.auth_key = APIAuth.objects.create(name="test")

    def get_api_result(self):
        url = reverse("session_staff_json")
        sig = self.get_signature(uri=url, method='GET', body='')
        rsp = self.client.get(url, **sig)
        self.assertEqual(OK, rsp.status_code)
        response_data = json.loads(rsp.content.decode('utf-8'))
        self.assertEqual(OK, response_data['code'])
        return response_data['data']

    def test_no_api_key(self):
        rsp = self.client.get(reverse("session_staff_json"))
        self.assertEqual(FORBIDDEN, rsp.status_code)

    def test_bad_api_key(self):
        self.auth_key.auth_key = 'who are you fooling?'
        url = reverse("session_staff_json")
        sig = self.get_signature(uri=url, method='GET', body='')
        rsp = self.client.get(url, **sig)
        self.assertEqual(FORBIDDEN, rsp.status_code)

    def test_bad_api_secret(self):
        self.auth_key.secret = 'who are you fooling?'
        url = reverse("session_staff_json")
        sig = self.get_signature(uri=url, method='GET', body='')
        rsp = self.client.get(url, **sig)
        self.assertEqual(FORBIDDEN, rsp.status_code)

    def test_no_data(self):
        data = self.get_api_result()
        self.assertEqual(0, len(data))

    def test_empty_session(self):
        self.session = SessionFactory()
        data = self.get_api_result()
        self.assertEqual(0, len(data))

    def test_slot_no_roles(self):
        session = SessionFactory()
        slot = SlotFactory()
        session.slots.add(slot)
        data = self.get_api_result()
        self.assertEqual(
            [{
                'conf_key': slot.pk,
                'chair_email': '',
                'chair_name': '',
                'runner_email': '',
                'runner_name': ''
            }],
            data
        )

    def test_slot_chair_no_runner(self):
        user = UserFactory(first_name="Melanie", last_name="Pickle", email='foo@example.com')
        session = SessionFactory()
        slot = SlotFactory()
        session.slots.add(slot)
        SessionRoleFactory(session=session, user=user, role=SessionRole.SESSION_ROLE_CHAIR)
        data = self.get_api_result()
        self.assertEqual(
            [{
                'conf_key': slot.pk,
                'chair_email': 'foo@example.com',
                'chair_name': 'Melanie Pickle',
                'runner_email': '',
                'runner_name': ''
            }],
            data
        )

    def test_slot_runner_no_chair(self):
        user = UserFactory(first_name="Melanie", last_name="Pickle", email='foo@example.com')
        session = SessionFactory()
        slot = SlotFactory()
        session.slots.add(slot)
        SessionRoleFactory(session=session, user=user, role=SessionRole.SESSION_ROLE_RUNNER)
        data = self.get_api_result()
        self.assertEqual(
            [{
                'conf_key': slot.pk,
                'chair_email': '',
                'chair_name': '',
                'runner_email': 'foo@example.com',
                'runner_name': 'Melanie Pickle',
            }],
            data
        )

    def test_slot_chair_and_runner(self):
        user1 = UserFactory(first_name="Melanie", last_name="Pickle", email='foo@example.com')
        user2 = UserFactory(first_name="Ichabod", last_name="Crane", email='crane@sleepyhollow.com')
        session = SessionFactory()
        slot = SlotFactory()
        session.slots.add(slot)
        SessionRoleFactory(session=session, user=user1, role=SessionRole.SESSION_ROLE_CHAIR)
        SessionRoleFactory(session=session, user=user2, role=SessionRole.SESSION_ROLE_RUNNER)
        data = self.get_api_result()
        self.assertEqual(
            [{
                'conf_key': slot.pk,
                'chair_email': 'foo@example.com',
                'chair_name': 'Melanie Pickle',
                'runner_email': 'crane@sleepyhollow.com',
                'runner_name': 'Ichabod Crane',
            }],
            data
        )

    def test_two_chairs_two_runners_one_declined(self):
        user1 = UserFactory(first_name="Melanie", last_name="Pickle", email='foo@example.com')
        user2 = UserFactory(first_name="Ichabod", last_name="Crane", email='crane@sleepyhollow.com')
        session = SessionFactory()
        slot = SlotFactory()
        session.slots.add(slot)
        SessionRoleFactory(session=session, user=user1, role=SessionRole.SESSION_ROLE_CHAIR)
        SessionRoleFactory(session=session, user=user2, role=SessionRole.SESSION_ROLE_CHAIR,
                           status=False)
        user3 = UserFactory(first_name="Mike", last_name="Hammer", email='noir@example.com')
        user4 = UserFactory(first_name="Sam", last_name="Spade", email='private@eye.com')
        SessionRoleFactory(session=session, user=user3, role=SessionRole.SESSION_ROLE_RUNNER)
        SessionRoleFactory(session=session, user=user4, role=SessionRole.SESSION_ROLE_RUNNER,
                           status=False)
        data = self.get_api_result()
        self.assertEqual(
            [{
                'conf_key': slot.pk,
                'chair_email': 'foo@example.com',
                'chair_name': 'Melanie Pickle',
                'runner_email': 'noir@example.com',
                'runner_name': 'Mike Hammer'
            }],
            data
        )

    def test_two_slots_one_session(self):
        # If there are two slots, we return data for each of them, in order of the slots
        # start time
        user1 = UserFactory(first_name="Melanie", last_name="Pickle", email='foo@example.com')
        user2 = UserFactory(first_name="Ichabod", last_name="Crane", email='crane@sleepyhollow.com')
        session = SessionFactory()
        slot1 = SlotFactory(start=datetime.time(13))
        slot2 = SlotFactory(start=datetime.time(8))
        session.slots.add(slot1)
        session.slots.add(slot2)
        SessionRoleFactory(session=session, user=user1, role=SessionRole.SESSION_ROLE_CHAIR)
        SessionRoleFactory(session=session, user=user2, role=SessionRole.SESSION_ROLE_CHAIR,
                           status=False)
        data = self.get_api_result()
        self.assertEqual(
            [{
                'conf_key': slot2.pk,
                'chair_email': 'foo@example.com',
                'chair_name': 'Melanie Pickle',
                'runner_email': '',
                'runner_name': ''
            }, {
                'conf_key': slot1.pk,
                'chair_email': 'foo@example.com',
                'chair_name': 'Melanie Pickle',
                'runner_email': '',
                'runner_name': ''
            }],
            data
        )

    def test_two_slots_two_sessions(self):
        # If there are two slots, we return data for each of them, in order of the slots
        # start time
        user1 = UserFactory(first_name="Melanie", last_name="Pickle", email='foo@example.com')
        user2 = UserFactory(first_name="Ichabod", last_name="Crane", email='crane@sleepyhollow.com')
        session1 = SessionFactory()
        session2 = SessionFactory()
        slot1 = SlotFactory(start=datetime.time(13))
        slot2 = SlotFactory(start=datetime.time(8))
        session1.slots.add(slot1)
        session2.slots.add(slot2)
        SessionRoleFactory(session=session1, user=user1, role=SessionRole.SESSION_ROLE_CHAIR)
        SessionRoleFactory(session=session1, user=user2, role=SessionRole.SESSION_ROLE_RUNNER)
        user3 = UserFactory(first_name="Mike", last_name="Hammer", email='noir@example.com')
        user4 = UserFactory(first_name="Sam", last_name="Spade", email='private@eye.com')
        SessionRoleFactory(session=session2, user=user3, role=SessionRole.SESSION_ROLE_CHAIR)
        SessionRoleFactory(session=session2, user=user4, role=SessionRole.SESSION_ROLE_RUNNER)
        data = self.get_api_result()
        self.assertEqual(
            [{
                'conf_key': slot2.pk,
                'chair_email': 'noir@example.com',
                'chair_name': 'Mike Hammer',
                'runner_email': 'private@eye.com',
                'runner_name': 'Sam Spade'
            }, {
                'conf_key': slot1.pk,
                'chair_email': 'foo@example.com',
                'chair_name': 'Melanie Pickle',
                'runner_email': 'crane@sleepyhollow.com',
                'runner_name': 'Ichabod Crane'
            }],
            data
        )
