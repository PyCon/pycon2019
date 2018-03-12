import logging

from django.db.models import Count, Sum
from django.conf import settings
from django.core.management.base import NoArgsCommand

from pycon.finaid.models import FinancialAidApplication
from pycon.finaid.utils import send_email_message

logger = logging.getLogger(__name__)


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        return
        result = FinancialAidApplication.objects.aggregate(Count('id'), Sum('amount_requested'))
        template_name = 'admin/weekly'
        send_email_message(template_name,
                           from_=settings.FINANCIAL_AID_EMAIL,
                           to=settings.FINANCIAL_AID_WEEKLY_REPORT_EMAIL,
                           context=result)
