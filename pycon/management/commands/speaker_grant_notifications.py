from collections import defaultdict

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from symposion.proposals.kinds import get_kind_slugs, get_proposal_model

from pycon.models import PyConProposal
from pycon.finaid.models import FinancialAidApplication, APPLICATION_TYPE_SPEAKER
from pycon.finaid.utils import has_application, send_email_message


SLUGS = get_kind_slugs()
DOMAIN = Site.objects.get_current().domain

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--kind', action='store', dest='kind', required=True,
                            help='Proposal Kind to notify: {}'.format(', '.join(SLUGS)))

    def handle(self, *args, **options):
        if options['kind'] not in SLUGS:
            print('ERROR: Unknown Proposal Kind: {}\n       Must be one of: {}'.format(options['kind'], ', '.join(SLUGS)))
            return False

        to_apply = defaultdict(list)
        to_confirm = defaultdict(list)

        accepted = get_proposal_model(options['kind']).objects.filter(overall_status=PyConProposal.STATUS_ACCEPTED)
        for proposal in accepted:
            if proposal.speaker.financial_support and has_application(proposal.speaker.user):
                application = FinancialAidApplication.objects.get(user=proposal.speaker.user)
                application.application_type = APPLICATION_TYPE_SPEAKER
                application.presenting = True
                application.save()
                path = reverse('speaker_grant_edit')
                url = 'https://{domain}{path}'.format(domain=DOMAIN, path=path)
                to_confirm[proposal.speaker.email].append(proposal)
            if proposal.speaker.financial_support and not has_application(proposal.speaker.user):
                path = reverse('speaker_grant_apply')
                url = 'https://{domain}{path}'.format(domain=DOMAIN, path=path)
                to_apply[proposal.speaker.email].append(proposal)

        for email, proposals in to_apply.items():
            send_email_message(
                'speaker_grant_apply',
                from_='pycon-aid@python.org',
                to=['pycon-aid@python.org', email],
                context={
                    'proposal_kind': options['kind'],
                    'user': proposals[0].speaker.user,
                    'domain': DOMAIN,
                    'proposal': proposals[0],
                },
            )
        for email, proposals in to_confirm.items():
            send_email_message(
                'speaker_grant_confirm',
                from_='pycon-aid@python.org',
                to=['pycon-aid@python.org', email],
                context={
                    'proposal_kind': options['kind'],
                    'user': proposals[0].speaker.user,
                    'domain': DOMAIN,
                    'proposal': proposals[0],
                },
            )
