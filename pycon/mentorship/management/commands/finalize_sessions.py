import argparse
import json
import random

import dateutil

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from pycon.mentorship.models import MentorshipSession
from pycon.mentorship.models import MentorshipMentee


class Command(BaseCommand):

    def handle(self, *args, **options):
        sessions = MentorshipSession.objects.filter(finalized=False)
        for session in sorted(sessions, key=lambda x: x.slot.time):
            if session.mentors.count() >= 2 and session.mentees.count() >= 3:
                if session.mentors.count() > 2:
                    for mentor in session.mentors.all()[2:]:
                        session.mentors.remove(mentor)
                if session.mentees.count() > 3:
                    for mentee in session.mentees.all()[3:]:
                        session.mentees.remove(mentee)
                session.finalize()

        sessions = MentorshipSession.objects.filter(finalized=False)
        for session in sorted(sessions, key=lambda x: x.slot.time):
            for mentor in session.mentors.all():
                if not mentor.available:
                    session.mentors.remove(mentor)
                    session.save()

        sessions = MentorshipSession.objects.filter(finalized=False)
        for session in sorted(sessions, key=lambda x: x.slot.time):
            session_mentors_count = session.mentors.count()
            if session_mentors_count == 0:
                session.delete()
                continue
            if session_mentors_count < 2:
                 mentors = session.available_mentors()
                 print(session.slot)
                 print(mentors)
                 session_mentors_count = session.mentors.count()
                 if len(mentors) + session_mentors_count < 2:
                     session.delete()
                 else:
                     for i in range(session_mentors_count, 2):
                         session.mentors.add(mentors[random.randint(0, 2-i)])

        unpaired = []
        for mentee in MentorshipMentee.objects.filter(responded=True):
            if mentee.potential_sessions_as_mentee.count() == 0 and mentee.assigned_sessions_as_mentee.count() == 0:
                unpaired.append(mentee)

        print(unpaired)
