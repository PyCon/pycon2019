from collections import defaultdict
from datetime import datetime, timedelta

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from symposion.proposals.kinds import get_kind_slugs, get_proposal_model
from symposion.utils.mail import send_email

SLUGS = get_kind_slugs()
DOMAIN = Site.objects.get_current().domain

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--kind', action='store', dest='kind', required=True,
                            help='Proposal Kind to bump: {}'.format(', '.join(SLUGS)))

    def handle(self, *args, **options):
        if options['kind'] not in SLUGS:
            print('ERROR: Unknown Proposal Kind: {}\n       Must be one of: {}'.format(options['kind'], ', '.join(SLUGS)))
            return False

        to_bump = defaultdict(list)

        unsubmitted = get_proposal_model(options['kind']).objects.filter(submitted=False, cancelled=False)
        for unsub in unsubmitted:
            path = reverse('proposal_detail', args=[unsub.id])
            url = 'https://{domain}{path}'.format(domain=DOMAIN, path=path)
            if unsub.created > datetime(year=2019, month=1, day=4, hour=7) - timedelta(days=4):
                to_bump[unsub.speaker.email].append(unsub)

        for email, proposals in to_bump.items():
            send_email(
                to=[email],
                kind='proposal_last_chance',
                context={
                    'proposal_kind': options['kind'],
                    'user': proposals[0].speaker.user,
                    'proposals': proposals,
                },
            )
