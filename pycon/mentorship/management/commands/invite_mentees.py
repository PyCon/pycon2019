
from django.core.management.base import BaseCommand

from symposion.speakers.models import Speaker

from pycon.mentorship.utils import send_email_message


class Command(BaseCommand):

    def handle(self, *args, **options):
        for speaker in Speaker.objects.exclude(interested_mentee__exact=''):
            send_email_message(
                "mentee_invitation",
                from_="pycon-mentorship@python.org",
                to=[speaker.email],
                context={}
            )
