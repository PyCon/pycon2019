import argparse
import json

import dateutil

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from pycon.mentorship.models import MentorshipSession


class Command(BaseCommand):

    def handle(self, *args, **options):
        sessions = MentorshipSession.objects.filter(finalized=False)
        for session in sorted(sessions, key=lambda x: x.slot.time):
            if session.mentors.count() >= 2 and session.mentees.count() >= 3:
                session.finalize()
