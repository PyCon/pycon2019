import datetime
import logging

from django.conf import settings
from django.core.management.base import NoArgsCommand

from pycon.finaid.models import Receipt

logger = logging.getLogger(__name__)


class Command(NoArgsCommand):

    def handle(self, *args, **options):
        if hasattr(settings, 'FIXER_ACCESS_KEY') and settings.FIXER_ACCESS_KEY is not None:
            converted = 0
            to_convert = Receipt.objects.filter(usd_amount=None).all()
            for receipt in to_convert:
                receipt.convert()
                receipt.save()
                converted += 1
            print('converted {} receipt currencies'.format(converted))
        else:
            print('fixer.io access key not configured')
