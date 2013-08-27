import json
import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from .decorators import api_view
from .models import ProposalData, IRCLogLine

from symposion.proposals.models import ProposalBase


@api_view
def proposal_list(request, filter=None):
    """Retrieve and return a list of proposals, optionally
    filtered by the given acceptance status.
    """
    # See if there is such a proposal
    proposals = ProposalBase.objects.all().order_by('pk')
    if filter:
        proposals = proposals.filter(result__status=filter)

    # If there's a limit parameter provided, limit to those objects.
    if 'limit' in request.GET:
        proposals = proposals[0:request.GET['limit']]

    # Return the proposal data objects.
    return [i.as_dict() for i in proposals]

@api_view
def proposal_detail(request, proposal_id):
    """Retrieve and return information about the given proposal.
    If this is a POST request, write the appropriate data instead.
    """
    # Retrieve the proposal.
    proposal = get_object_or_404(ProposalBase, pk=int(proposal_id))

    # If this is a POST request, then we are **setting** data
    # on this proposal; do that.
    if request.method == 'POST':
        data = json.loads(request.body)

        # If we get a dictionary (which will be the normal case), then 
        # look for certain "special" keys, and if we get them, we alter some
        # status on the proposal itself.
        if isinstance(data, dict):
            status = data.pop('status', None)
            if status:
                # FIXME: Write this!
                pass

        # Anything else just becomes arbitrary proposal data.
        pd, new = ProposalData.objects.get_or_create(proposal=proposal)
        pd.data = json.dumps(data)
        pd.save()

        # Return a success.
        return ({ 'message': 'Proposal updated.' }, 202)

    # Return a dictionary representation of the proposal.
    return proposal.as_dict(details=True)

@api_view
def proposal_irc_logs(request, proposal_id):
    """Write or retrieve the IRC logs for a given proposal.

    If writing logs, each log entry must have the following
    JSON format:
        {
            'user': '(text identifying the user)',
            'line': '(the IRC line)',
            'timestamp': '%Y-%m-%d %H:%M:%S.%f',
        }
    """
    # Retrieve the proposal.
    proposal = get_object_or_404(ProposalBase, pk=int(proposal_id))

    # If we are writing logs, do that.
    if request.method == 'POST':
        logs = json.loads(request.body)

        # Add each log entry.
        for log in logs:
            IRCLogLine.objects.create(
                line=log['line'],
                proposal=proposal,
                user=log['user'],
                timestamp=log['timestamp'],
            )

        # Done; send back a success.
        return ({ 'message': 'Log entry added.' }, 201)

    # This is a retrieval request; get the logs associated with
    # this proposal and send them back.
    fields = ('line', 'proposal_id', 'timestamp', 'user')
    logs = list(IRCLogLine.objects.filter(proposal=proposal)
                .order_by('timestamp').values(*fields))

    # Return the data.
    return logs
