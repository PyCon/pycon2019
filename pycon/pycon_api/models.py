import pytz
import uuid

from calendar import timegm
from datetime import datetime
from hashlib import sha1

from django.db import models
from django.utils.translation import ugettext_lazy as _

from pycon.pycon_api.exceptions import AuthenticationError
from symposion.proposals.models import ProposalBase


class APIAuth(models.Model):
    """API Users need to have a record in this table"""
    name = models.CharField(
        help_text='Description of person or service using the API key.',
        max_length=100,
    )
    auth_key = models.CharField(
        default=lambda: str(uuid.uuid4()),
        max_length=36,
        unique=True,
    )
    secret = models.CharField(
        default=lambda: str(uuid.uuid4()),
        max_length=36,
    )
    enabled = models.BooleanField(default=True)

    @classmethod
    def verify_request(cls, request):
        """Return True if a request is properly signed, and may
        be safely executed; raise AuthenticationError otherwise.
        """
        # Sanity check: If there's no API key in the headers at all,
        # then we know right away we don't have a valid signature.
        if 'HTTP_X_API_KEY' not in request.META:
            raise AuthenticationError('API Key not provided.')

        # Retrieve the authorization key; if it's not found, provide
        # an error to that effect.
        try:
            auth_instance = cls.objects.get(
                auth_key=request.META['HTTP_X_API_KEY'],
                enabled=True,
            )
        except cls.DoesNotExist:
            raise AuthenticationError('The API Key provided is not valid.')

        # Sanity check: Was a signature of some sort also provided?
        # If there is no signature, then it can't be valid.
        if 'HTTP_X_API_SIGNATURE' not in request.META:
            raise AuthenticationError('No signature provided.')
        if 'HTTP_X_API_TIMESTAMP' not in request.META:
            raise AuthenticationError('API Timestamp not provided.')

        # Ensure that the timestamp is within ten minutes of
        # the current time.
        unix_now = timegm(datetime.now(tz=pytz.UTC).timetuple())
        request_timestamp = int(request.META['HTTP_X_API_TIMESTAMP'])
        if abs(unix_now - request_timestamp) > 600:
            raise AuthenticationError('Request is not current.')

        # OK, now duplicate the expected request signature.
        base_string = unicode(''.join((
            auth_instance.secret,
            unicode(request_timestamp),
            request.method.upper(),
            request.get_full_path(),
            request.body,
        )))
        expected_signature = sha1(base_string.encode('utf-8')).hexdigest()

        # Ensure that the actual request signature matches
        # the one we recieved, and raise AuthenticationError if it does not.
        if expected_signature != request.META['HTTP_X_API_SIGNATURE']:
            raise AuthenticationError('Invalid signature.')

        # Everything is fine.
        return True


class ProposalData(models.Model):
    """A chunk of text data associated with a proposal"""
    # Probably JSON, but doesn't have to be
    proposal = models.OneToOneField(ProposalBase, db_index=True,
                                    related_name='data')
    data = models.TextField()


class IRCLogLine(models.Model):
    timestamp = models.DateTimeField()
    proposal = models.ForeignKey(ProposalBase)
    user = models.CharField(max_length=40)
    line = models.TextField(blank=True)
