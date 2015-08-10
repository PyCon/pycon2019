import datetime
import json
import pytz
import uuid

from calendar import timegm
from hashlib import sha1
from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import FakePayload
from django.utils.encoding import force_str

from pycon.models import PyConTalkProposal, ThunderdomeGroup
from pycon.tests.factories import PyConTalkProposalFactory, ThunderdomeGroupFactory, \
    ProposalResultFactory

from .models import APIAuth, ProposalData, IRCLogLine
from .decorators import DATETIME_FORMAT


class RawDataClientMixin(object):
    """Mix this into a TestCase class to be able to post raw data through
    the test client.
    """
    def post_raw_data(self, path, post_data):
        """
        The built-in test client's post() method assumes the data you pass
        is a dictionary and encodes it. If we just want to pass the data
        unmodified, we need our own version of post().
        """
        parsed = urlparse(path)
        r = {
            'CONTENT_LENGTH': len(post_data),
            'CONTENT_TYPE':   "text/plain",
            'PATH_INFO':      self.client._get_path(parsed),
            'QUERY_STRING':   force_str(parsed[4]),
            'REQUEST_METHOD': str('POST'),
            'wsgi.input':     FakePayload(post_data),
        }

        # Add the request signature to the headers being sent.
        r.update(self.get_signature(path, method='POST', body=post_data))

        # Make the actual request.
        return self.client.request(**r)

    def get_signature(self, uri, method='GET', body=''):
        """Return a dictionary with the API key and API get_signature
        to be sent for the given request."""
        # What time is it now?
        timestamp = timegm(datetime.datetime.now(tz=pytz.UTC).timetuple())

        # Calculate the base string to use for the signature.
        base_string = unicode(''.join((
            self.auth_key.secret,
            unicode(timestamp),
            method.upper(),
            uri,
            body,
        ))).encode('utf-8')

        # Return a dictionary with the headers to send.
        return {
            'HTTP_X_API_KEY': self.auth_key.auth_key,
            'HTTP_X_API_SIGNATURE': sha1(base_string).hexdigest(),
            'HTTP_X_API_TIMESTAMP': timestamp,
        }


class ThunderdomeGroupListApiTest(RawDataClientMixin, TestCase):
    def setUp(self):
        self.auth_key = APIAuth.objects.create(name="test")
        self.url = reverse('thunderdome_groups')

    def test_get_some(self):
        ThunderdomeGroupFactory(label='curly', code='3')
        ThunderdomeGroupFactory(label='larry', code='2')
        ThunderdomeGroupFactory(label='moe', code='1')
        rsp = self.client.get(self.url, **self.get_signature(self.url))
        self.assertEqual(200, rsp.status_code)
        data = json.loads(rsp.content)
        groups = data['data']
        # We got the 3 groups, in order by code
        self.assertEqual(groups[0]['label'], 'moe')
        self.assertEqual(groups[1]['label'], 'larry')
        self.assertEqual(groups[2]['label'], 'curly')

    def test_get_undecided(self):
        ThunderdomeGroupFactory(label='curly', code='3')
        ThunderdomeGroupFactory(label='larry', code='2', decided=True)
        ThunderdomeGroupFactory(label='moe', code='1', decided=True)
        url = self.url + "?undecided=1"
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(200, rsp.status_code)
        data = json.loads(rsp.content)
        groups = data['data']
        self.assertEqual(1, len(groups))
        self.assertEqual('curly', groups[0]['label'])


class ThunderdomeGroupAddApiTest(RawDataClientMixin, TestCase):
    def setUp(self):
        self.auth_key = APIAuth.objects.create(name="test")
        self.url = reverse('thunderdome_group_add')

    def test_get(self):
        # This is post-only
        rsp = self.client.get(self.url, **self.get_signature(self.url))
        self.assertEqual(405, rsp.status_code)

    def test_make_one(self):
        data = {
            'label': 'My_label',
            'code': 'My_code'
        }
        rsp = self.post_raw_data(self.url, json.dumps(data))
        self.assertEqual(201, rsp.status_code)
        group = ThunderdomeGroup.objects.get()
        self.assertEqual(group.code, 'my-code')  # _ changes to - and all lowered
        self.assertEqual(group.label, 'My_label')
        # Response includes the modified code
        code = json.loads(rsp.content)['data']['code']
        self.assertEqual(code, group.code)

    def test_missing_label(self):
        data = {
            'code': 'My_code'
        }
        rsp = self.post_raw_data(self.url, json.dumps(data))
        self.assertEqual(400, rsp.status_code)

    def test_missing_code(self):
        data = {
            'label': 'My_label',
        }
        rsp = self.post_raw_data(self.url, json.dumps(data))
        self.assertEqual(400, rsp.status_code)


class ThunderdomeGroupDecideTest(RawDataClientMixin, TestCase):
    def setUp(self):
        self.group = ThunderdomeGroupFactory(code='fred')
        self.auth_key = APIAuth.objects.create(name="test")
        self.url = reverse('thunderdome_group_decide', args=(self.group.code,))
        self.talk1 = PyConTalkProposalFactory(thunderdome_group=self.group)
        self.talk2 = PyConTalkProposalFactory(thunderdome_group=self.group)

        ProposalResultFactory(proposal=self.talk1, status="undecided")
        ProposalResultFactory(proposal=self.talk2, status="undecided")

    def test_get(self):
        # This is post-only
        rsp = self.client.get(self.url, **self.get_signature(self.url))
        self.assertEqual(405, rsp.status_code)

    def test_no_such_group(self):
        bad_id = self.group.id + 1
        url = reverse('thunderdome_group_decide', args=(self.group.id,))
        rsp = self.post_raw_data(url, '')
        self.assertEqual(400, rsp.status_code, rsp.content.decode('utf-8'))

    def test_undeciding_a_group(self):
        # If no talk statuses are provided, all talk statuses should
        # change to standby
        data = {}
        rsp = self.post_raw_data(self.url, json.dumps(data))
        self.assertEqual(202, rsp.status_code, rsp.content.decode('utf-8'))
        group = ThunderdomeGroup.objects.get(id=self.group.id)

    def test_not_all_talks(self):
        # We only process if all talks in the group have a new status provided
        data = {
            'talks': [
                (self.talk1.id, 'accepted'),
            ]
        }
        rsp = self.post_raw_data(self.url, json.dumps(data))
        self.assertEqual(400, rsp.status_code, rsp.content.decode('utf-8'))

    def test_update_talk_statuses(self):
        data = {
            'talks': [
                (self.talk1.id, 'accepted'),
                (self.talk2.id, 'rejected')
            ]
        }
        rsp = self.post_raw_data(self.url, json.dumps(data))
        talk1 = PyConTalkProposal.objects.get(id=self.talk1.id)
        self.assertEqual('accepted', talk1.result.status)
        talk1 = PyConTalkProposal.objects.get(id=self.talk2.id)
        self.assertEqual('rejected', talk1.result.status)


class PyConIRCLogsApiTest(TestCase, RawDataClientMixin):
    def setUp(self):
        self.auth_key = APIAuth.objects.create(name="test")
        self.proposal = PyConTalkProposalFactory.create()

    def test_get_logs_bad_auth(self):
        # Bad auth key
        auth_key = uuid.uuid4()  # random key
        url = reverse('proposal_irc_logs',
                      kwargs={'proposal_id': str(self.proposal.id)})
        rsp = self.client.get(url, HTTP_X_API_KEY=str(auth_key))
        self.assertEqual(403, rsp.status_code)
        self.assertEqual(
            json.loads(rsp.content)['error'],
            'The API Key provided is not valid.',
        )

    def test_get_logs_disabled_auth(self):
        # Auth disabled
        self.auth_key.enabled = False
        self.auth_key.save()
        url = reverse('proposal_irc_logs',
            kwargs={'proposal_id': str(self.proposal.id)}
        )
        rsp = self.client.get(url, HTTP_X_API_KEY=self.auth_key.auth_key)
        self.assertEqual(403, rsp.status_code)
        self.assertEqual(
            json.loads(rsp.content)['error'],
            'The API Key provided is not valid.',
        )

    def test_get_logs_no_data(self):
        # No logs for that proposal
        url = reverse('proposal_irc_logs', kwargs={
            'proposal_id': str(self.proposal.id),
        })
        rsp = self.client.get(url, **self.get_signature(url))


        self.assertEqual(200, rsp.status_code, rsp.content)
        logs = json.loads(rsp.content)['data']
        self.assertEqual([], logs)

    def test_get_logs_bad_proposal(self):
        # Proposal does not exist
        self.proposal.delete()
        url = reverse('proposal_irc_logs', kwargs={
            'proposal_id': str(self.proposal.id),
        })
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(404, rsp.status_code)

    def test_get_logs_data(self):
        # Get a couple of lines

        # Create the lines we'll get
        LINE1 = "Now is the time for all good folks to dance."
        LINE2 = "A completely different log line"
        USER1 = "Jim Bob"
        USER2 = "George Washington"
        now = datetime.datetime.now()
        # make sure they have different timestamps, and that microseconds
        # are preserved
        then = now + datetime.timedelta(microseconds=1)
        IRCLogLine.objects.create(proposal=self.proposal, line=LINE1,
                                  user=USER1,
                                  timestamp=now.strftime(DATETIME_FORMAT))
        IRCLogLine.objects.create(proposal=self.proposal, line=LINE2,
                                  user=USER2,
                                  timestamp=then.strftime(DATETIME_FORMAT))

        # Create another proposal and a line to make sure we
        # don't get it in the results
        self.proposal2 = PyConTalkProposalFactory.create()
        later = then + datetime.timedelta(seconds=2)
        IRCLogLine.objects.create(proposal=self.proposal2, line="wrong",
                                  user="wrong",
                                  timestamp=later.strftime(DATETIME_FORMAT))

        url = reverse('proposal_irc_logs', kwargs={
            'proposal_id': str(self.proposal.id),
        })
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(200, rsp.status_code)
        logs = json.loads(rsp.content)['data']
        self.assertEqual(2, len(logs))
        # They should come out in timestamp order. Data, including time
        # to the microsecond, should be preserved.
        self.assertEqual(LINE1, logs[0]['line'])
        self.assertEqual(USER1, logs[0]['user'])
        self.assertEqual(now.strftime(DATETIME_FORMAT), logs[0]['timestamp'])
        self.assertEqual(LINE2, logs[1]['line'])
        self.assertEqual(then.strftime(DATETIME_FORMAT), logs[1]['timestamp'])
        self.assertEqual(USER2, logs[1]['user'])

    def test_set_data(self):
        # We can set data and it ends up in the database
        url = reverse('proposal_irc_logs', kwargs={
            'proposal_id': str(self.proposal.id)
        })
        now = datetime.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        LINE = "Now is the time for all good folks to dance."
        USER = "Jim Bob"
        logs = [
            {
                'timestamp': now_formatted,
                'line': LINE,
                'user': USER,
            }
        ]
        json_data = json.dumps(logs)
        rsp = self.post_raw_data(url, post_data=json_data)
        self.assertEqual(201, rsp.status_code, rsp.content)

        # Should only be one log entry
        log = IRCLogLine.objects.get()
        self.assertEqual(self.proposal.id, log.proposal_id)
        self.assertEqual(LINE, log.line)
        self.assertEqual(now, log.timestamp)
        self.assertEqual(USER, log.user)

    def test_set_data_bad_proposal(self):
        # proposal does not exist
        url = reverse('proposal_irc_logs', kwargs={
            'proposal_id': 999,
        })
        now = datetime.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        LINE = "Now is the time for all good folks to dance."
        USER = "Jim Bob"
        logs = [
            {
                'timestamp': now_formatted,
                'line': LINE,
                'user': USER,
            }
        ]
        json_data = json.dumps(logs)
        rsp = self.post_raw_data(url, post_data=json_data)
        self.assertEqual(404, rsp.status_code)


class PyConProposalDataApiTest(TestCase, RawDataClientMixin):
    def setUp(self):
        self.auth_key = APIAuth.objects.create(name="test")
        self.proposal = PyConTalkProposalFactory.create()

    def test_get_data_bad_auth(self):
        auth_key = uuid.uuid4()
        # If proposal has no data, we get back an empty string.
        url = reverse('proposal_detail', kwargs={ 
            'proposal_id': self.proposal.id,
        })
        rsp = self.client.get(url)
        self.assertEqual(403, rsp.status_code)
        self.assertEqual(
            json.loads(rsp.content)['error'],
            'API Key not provided.',
        )

    def test_get_data_disabled_auth(self):
        self.auth_key.enabled = False
        self.auth_key.save()
        url = reverse('proposal_detail', kwargs={
            'proposal_id': self.proposal.id,
        })
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(403, rsp.status_code)
        self.assertEqual(
            json.loads(rsp.content)['error'],
            'The API Key provided is not valid.',
        )

    def test_get_data(self):
        # If proposal has data, we get it.
        TEST_DATA = 'now is the time for all good people...'
        ProposalData.objects.create(proposal=self.proposal,
                                    data=json.dumps(TEST_DATA)),
        url = reverse('proposal_detail', kwargs={
            'proposal_id': self.proposal.id,
        })
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(200, rsp.status_code, rsp.content)
        self.assertEqual(TEST_DATA, json.loads(rsp.content)['data']['extra'])

    def test_set_data(self):
        # We can set data and it ends up in the database
        url = reverse('proposal_detail', kwargs={
            'proposal_id': self.proposal.id,
        })
        TEST_DATA = {'stuff': 'Foo! Bar! Sis boom bah!'}
        rsp = self.post_raw_data(url, post_data=json.dumps(TEST_DATA))
        self.assertEqual(202, rsp.status_code, rsp.content)
        proposal = PyConTalkProposal.objects.get(id=self.proposal.id)
        self.assertEqual(TEST_DATA, json.loads(proposal.data.data))

    def test_replace_data(self):
        # If data already exists, a set replaces it
        TEST_DATA = {'stuff': 'now is the time for all good people...'}
        ProposalData.objects.create(proposal=self.proposal,
                                    data=TEST_DATA)
        url = reverse('proposal_detail', kwargs={
            'proposal_id': self.proposal.id,
        })
        TEST_DATA = {'stuff': 'Foo! Bar! Sis boom bah!'}
        rsp = self.post_raw_data(url, post_data=json.dumps(TEST_DATA))
        self.assertEqual(202, rsp.status_code, rsp.content)
        proposal = PyConTalkProposal.objects.get(id=self.proposal.id)
        self.assertEqual(TEST_DATA, json.loads(proposal.data.data))

    def test_round_trip(self):
        # We can set data using the API, and get it back using the API
        url = reverse('proposal_detail', kwargs={
            'proposal_id': self.proposal.id,
        })
        TEST_DATA = {'stuff': 'Foo! Bar! Sis boom bah!'}
        rsp = self.post_raw_data(url, post_data=json.dumps(TEST_DATA))
        self.assertEqual(202, rsp.status_code, rsp.content)

        # Now establish that we can get it back.
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(200, rsp.status_code)
        self.assertEqual(TEST_DATA, json.loads(rsp.content)['data']['extra'])

    def test_get_no_proposal(self):
        # If there's no such proposal, we get back a 404
        url = reverse('proposal_detail', kwargs={
            'proposal_id': str(self.proposal.id) + "0099",
        })
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(404, rsp.status_code)

    def test_get_bad_auth(self):
        # Bad auth key fails
        bad_auth_key = uuid.uuid4()  # another random key, it will not match
        url = reverse('proposal_detail', kwargs={
            'proposal_id': self.proposal.id,
        })
        rsp = self.client.get(url, HTTP_X_API_KEY=str(bad_auth_key))
        self.assertEqual(403, rsp.status_code)

    def test_list_view(self):
        url = reverse('proposal_list')
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(rsp.status_code, 200, rsp.content)
        self.assertEqual(len(json.loads(rsp.content)['data']), 1)

    def test_list_view_talks_only(self):
        url = reverse('proposal_list') + '?type=talk'
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(rsp.status_code, 200, rsp.content)
        self.assertEqual(len(json.loads(rsp.content)['data']), 1)

    def test_list_view_tutorials_only(self):
        url = reverse('proposal_list') + '?type=tutorial'
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(rsp.status_code, 200, rsp.content)
        self.assertEqual(len(json.loads(rsp.content)['data']), 0)

    def test_list_view_undecided_only(self):
        url = reverse('proposal_list') + '?status=undecided'
        rsp = self.client.get(url, **self.get_signature(url))
        self.assertEqual(rsp.status_code, 200, rsp.content)
        self.assertEqual(len(json.loads(rsp.content)['data']), 1)

