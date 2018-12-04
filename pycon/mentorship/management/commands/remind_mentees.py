
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from symposion.speakers.models import Speaker

from pycon.mentorship.utils import send_email_message


class Command(BaseCommand):

    def handle(self, *args, **options):
        for speaker in Speaker.objects.exclude(interested_mentee__exact=''):
            try:
                mentee = speaker.user.mentorship_mentee.get(user=speaker.user)
                if mentee.responded:
                    continue
            except ObjectDoesNotExist:
                pass
            send_email_message(
                "mentee_reminder",
                from_="pycon-mentorship@python.org",
                to=[speaker.email],
                context={},
                bcc=False,
            )
