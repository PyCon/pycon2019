import json

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .decorators import api_view
from .models import ProposalData, IRCLogLine

from pycon.models import (PyConTalkProposal, PyConTutorialProposal,
            PyConLightningTalkProposal, PyConPosterProposal,
            ThunderdomeGroup)

from symposion.proposals.models import ProposalBase


PROPOSAL_TYPES = {
    'talk': PyConTalkProposal,
    'tutorial': PyConTutorialProposal,
    'lightning': PyConLightningTalkProposal,
    'poster': PyConPosterProposal,
}


@csrf_exempt
@api_view
def thunderdome_group_add(request):
    """Add a thunderdome group."""

    # If this isn't a POST request, fail out.
    if request.method != 'POST':
        return ({ 'error': 'POST request required.' }, 405)

    # Load our data.
    # For some bizarre reason that I cannot comprehend, request.body
    # has to be loaded twice.
    data = json.loads(request.body)
    if isinstance(data, (str, unicode)):
        data = json.loads(data)

    # Sanity check: Are a label and code present?
    for key in ('label', 'code'):
        if key not in data:
            return ({ 'error': 'Missing key: `%s`.' % key }, 400)

    # Create the thunderdome group.
    td_group = ThunderdomeGroup.objects.create(
        label=data['label'],
        code=data['code'].lower().replace(' ', '-').replace('_', '-'),
    )

    # Return back a success
    return ({ 'message': 'success', 'code': td_group.code }, 201)


@api_view
def thunderdome_group_list(request):
    """Retrieve and return a list of thunderdome groups, optionally filtering
    out decided groups.
    """
    groups = ThunderdomeGroup.objects.order_by('code')

    # If we were told to filter out decided groups, do so.
    undecided = request.GET.get('undecided', '').lower() in ('true', '1')
    if undecided:
        groups = groups.exclude(decided=True)

    # Return the results.
    return [i.as_dict for i in groups]


@csrf_exempt
@api_view
def thunderdome_group_decide(request, td_group_code):
    """Decide (or undecide) the talks in the given thunderdome group,
    and return a representation of the group after those updates are made.
    """
    # If this isn't a POST request, fail out.
    if request.method != 'POST':
        return ({ 'error': 'POST request required.' }, 405)

    # Get the thunderdome group we're working with.
    try:
        td_group = ThunderdomeGroup.objects.get(code=td_group_code)
    except ThunderdomeGroup.DoesNotExist:
        return ({'error': 'Invalid group: `%s`.' % td_group_code}, 400)

    # Load our data.
    # For some bizarre reason that I cannot comprehend, request.body
    # has to be loaded twice.
    data = json.loads(request.body)
    if isinstance(data, (str, unicode)):
        data = json.loads(data)

    # Sanity check: Are any talk statuses provided?
    # If not, we are **undeciding** this thunderdome group.
    if not data.get('talks', ()):
        td_group.decided = False
        for talk in td_group.talks.all():
            talk.result.status = 'standby'
            talk.result.save()
        return {
            'message': 'Thunderdome group undecided.',
            'thunderdome_group': td_group.as_dict, 
        }, 202

    # Sanity check: are all talks present?
    # If not, cowardly refuse to do anything.
    provided_talk_ids = set([int(i[0]) for i in data['talks']])
    expected_talk_ids = set([i.id for i in td_group.talks.all()])
    if provided_talk_ids != expected_talk_ids:
        return {'error': 'To set talks, a new status must be supplied '
                         'for EVERY talk in the group.\n'
                         'Missing: %s' % expected_talk_ids.difference(
                                            provided_talk_ids,
                                         )}

    # Iterate over each of the talks in this TD group, and set their
    # new status.
    for talk_id, status in data['talks']:
        talk = PyConTalkProposal.objects.get(id=int(talk_id))
        talk.result.status = status
        talk.result.save()

    # We're done; set this group to decided.
    td_group.decided = True
    td_group.save()

    # Return back things.
    return {
        'message': 'Thunderdome group decided.',
        'thunderdome_group': td_group.as_dict, 
    }, 202


@api_view
def proposal_list(request):
    """Retrieve and return a list of proposals, optionally
    filtered by the given acceptance status.
    """
    # What model should we be pulling from?
    model = ProposalBase
    proposal_type = request.GET.get('type', 'talk')
    if proposal_type:
        try:
            model = PROPOSAL_TYPES[proposal_type]
        except KeyError:
            return ({ 'error': 'unrecognized proposal type' }, 400)

    # See if there is such a proposal
    proposals = model.objects.select_related('result').order_by('pk')

    # Don't look at cancelled proposals.
    proposals = proposals.exclude(cancelled=True)

    # If specific proposal status is being requested, filter on that.
    desired_status = request.GET.get('status', None)
    if desired_status == 'undecided':
        proposals = proposals.filter(Q(result__status=desired_status) |
                                     Q(result=None))
    else:
        proposals = proposals.filter(result__status=desired_status)

    # We may be asking only for ungrouped talks; if so, limit to these.
    ungrouped = request.GET.get('ungrouped', '').lower() in ('true', '1')
    if ungrouped:
        proposals = proposals.filter(thunderdome_group=None)

    # If there's a limit parameter provided, limit to those objects.
    if 'limit' in request.GET:
        proposals = proposals[0:request.GET['limit']]

    # Return the proposal data objects.
    return [i.as_dict() for i in proposals]


@csrf_exempt
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
        # For some bizarre reason that I cannot comprehend, request.body
        # has to be loaded twice.
        data = json.loads(request.body)
        if isinstance(data, (str, unicode)):
            data = json.loads(data)

        # If we get a dictionary (which will be the normal case), then 
        # look for certain "special" keys, and if we get them, we alter some
        # status on the proposal itself.
        if isinstance(data, dict):
            # Check for the "status" key.  This assigns the given status
            # to the proposal.
            status = data.pop('status', None)
            if status:
                # Sanity check: Is this a valid value?
                if status not in ('accepted', 'rejected',
                                  'standby', 'undecided'):
                    return ({ 'error': 'Invalid status.' }, 400)

                proposal.result.status = status
                proposal.result.save()

            # Check for the "thunderdome_group" key.  This assigns the
            # given thunderdome group to the proposal.
            td_group_code = data.pop('thunderdome_group', None)
            if td_group_code:
                try:
                    td_group = ThunderdomeGroup.objects.get(code=td_group_code)
                except ThunderdomeGroup.DoesNotExist:
                    return ({ 'error': 'Invalid thunderdome group.' }, 400)

                proposal.pycontalkproposal.thunderdome_group = td_group
                proposal.pycontalkproposal.save()

        # Anything else just becomes arbitrary proposal data.
        pd, new = ProposalData.objects.get_or_create(proposal=proposal)
        pd.data = json.dumps(data)
        pd.save()

        # Return a success.
        return ({ 'message': 'Proposal updated.' }, 202)

    # Return a dictionary representation of the proposal.
    try:
        return proposal.pycontalkproposal.as_dict(details=True)
    except PyConTalkProposal.DoesNotExist:
        return proposal.as_dict(details=True)


@csrf_exempt
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
