import json
import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET, require_POST

from .models import ProposalData, APIAuth, IRCLogLine

from symposion.proposals.models import ProposalBase


# Format we'll use in JSON for datetimes
# Includes microseconds
# YYYY-MM-DD HH:MM:ss.uuuuuu
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


# We need to be able to serialize a datetime object, which the built-in
# encoder won't do. We also want to be sure to use a known format that
# preserved microseconds.
class JSONDatetimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime(DATETIME_FORMAT)
        else:
            return super(JSONDatetimeEncoder, self).default(o)


@require_POST
def set_proposal_data(request, auth_key, proposal_id):
    """
    Set the text data associated with a proposal. If the proposal already
    has data associated, the previous data is replaced by the new data.

    Takes two required parameters in the URL:

        auth_key - a valid API auth key
        proposal_id - database ID of the desired proposal (int)

    e.g.

        POST /pycon_api/set_proposal_data/<auth_key>/27/

    The request body should be the new text data to set.

    If the request is invalid, the response status is 400 or 401, and
    the response body is an error message.

    If the proposal is not found, response status is 404 and the
    response body is an error message (should help distinguish from
    a 404 due to using a bad URL).

    If the data is successfully set, response status is 200.
    """
    if not APIAuth.check_key(auth_key):
        return HttpResponse(content="Not authorized",
                            content_type="text/plain",
                            status=401)

    # See if there is such a proposal
    try:
        proposal = ProposalBase.objects.get(pk=proposal_id)
    except ProposalBase.DoesNotExist:
        return HttpResponseNotFound("proposal %s not found" % proposal_id)

    # get or create a ProposalData object
    obj, created = ProposalData.objects.get_or_create(
        proposal_id=proposal.id,
        defaults={
            'data': request.body,
        }
    )
    if not created:
        obj.data = request.body
        obj.save()
    return HttpResponse()


@require_GET
def get_proposal_data(request, auth_key, proposal_id):
    """
    Get the data associated with a proposal.

    Takes two required parameters as part of the URL:

        auth_key - a valid API auth key
        proposal_id - database ID of the desired proposal (int)

    e.g.

        GET /pycon_api/get_proposal_data/<auth_key>/27/

    If the request is invalid, the response status is 400 or 401, and
    the response body is an error message.

    If the proposal is not found, response status is 404 and the
    response body is an error message (should help distinguish from
    a 404 due to using a bad URL).

    If the proposal is found but has no data, then status is 200 and
    the returned body has length zero.

    If data is found, status is 200 and the response body is the data
    associated with the proposal.
    """

    if not APIAuth.check_key(auth_key):
        return HttpResponse(content="Not authorized",
                            content_type="text/plain",
                            status=401)

    # See if there is such a proposal
    try:
        proposal = ProposalBase.objects.get(pk=proposal_id)
    except ProposalBase.DoesNotExist:
        return HttpResponseNotFound("proposal not found")

    # The proposal exists - see if we have data for it
    try:
        data_record = proposal.data
    except ProposalData.DoesNotExist:
        data = ""
    else:
        data = data_record.data
    return HttpResponse(content=data,
                        content_type="text/plain",
                        status=200)


@require_POST
def set_irc_logs(request, auth_key):
    """
    Add some IRC log lines associated with proposals.

    Takes one required parameter in the URL:

        auth_key - a valid API auth key

    e.g.

        POST /pycon_api/set_irc_logs/<auth_key>/

    If the request is invalid, the response status is 400 or 401, and
    the response body is an error message.

    If the proposal is not found, response status is 404 and the
    response body is an error message (should help distinguish from
    a 404 due to using a bad URL).

    If the data is successfully set, response status is 200.

    The request body should contain the log data formatted as JSON, as
    an array of dictionaries, each with four keys:

        {
            'proposal_id': (id of proposal),   # integer
            'user': '(text identifying the user)',
            'line': '(the IRC line)',
            'timestamp': '(timestamp - format is below
        }

    The timestamp format must be `YYYY-MM-DD HH:MM:ss.uuuuuu`, which you
    can get using Python strftime with the format ``"%Y-%m-%d %H:%M:%S.%f"``.

    """
    if not APIAuth.check_key(auth_key):
        return HttpResponse(content="Not authorized",
                            content_type="text/plain",
                            status=401)
    logs = json.loads(request.body)

    # validate proposal IDs
    validated_ids = set()
    for log in logs:
        proposal_id = int(log['proposal_id'])
        if proposal_id not in validated_ids:
            if not ProposalBase.objects.filter(pk=proposal_id).exists():
                return HttpResponseNotFound("proposal %s not found"
                                            % proposal_id)
            validated_ids.add(proposal_id)

    # Proposal IDs look good, add the logs
    for log in logs:
        IRCLogLine.objects.create(
            proposal_id=log['proposal_id'],
            user=log['user'],
            timestamp=log['timestamp'],
            line=log['line']
        )
    return HttpResponse()


@require_GET
def get_irc_logs(request, auth_key, proposal_id):
    """
    Get the IRC logs associated with a proposal, in timestamp order.

    Takes two required parameters as part of the URL:

        auth_key - a valid API auth key
        proposal_id - database ID of the desired proposal (int)

    e.g.

        GET /pycon_api/get_irc_logs/<auth_key>/27/

    If the request is invalid, the response status is 400 or 401, and
    the response body is an error message.

    If the proposal is not found, response status is 404 and the
    response body is an error message (should help distinguish from
    a 404 due to using a bad URL).

    If data is found, status is 200 and the response body IS the data
    associated with the proposal, formatted in JSON in the same format
    that set_irc_logs takes on input.
    """

    if not APIAuth.check_key(auth_key):
        return HttpResponse(content="Not authorized",
                            content_type="text/plain",
                            status=401)

    # See if there is such a proposal
    try:
        proposal = ProposalBase.objects.get(pk=proposal_id)
    except ProposalBase.DoesNotExist:
        return HttpResponseNotFound("proposal not found")

    fields = ['timestamp', 'user', 'line', 'proposal_id']
    logs = list(IRCLogLine.objects.filter(proposal=proposal)
                .order_by('timestamp').values(*fields))

    json_data = json.dumps(logs, cls=JSONDatetimeEncoder)
    return HttpResponse(content=json_data,
                        content_type="application/json",
                        status=200)
