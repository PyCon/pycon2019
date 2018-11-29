import argparse
import datetime
import json
import random

import dateutil

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from pycon.mentorship.models import MentorshipSession
from pycon.mentorship.models import MentorshipMentee

from pycon.mentorship.utils import send_email_message


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
                addresses = [str(x) for x in session.mentees.all()] + [str(x) for x in session.mentors.all()]
                send_email_message(
                    "session_confirmed",
                    from_="pycon-mentorship@python.org",
                    to=addresses,
                    context={
                        "mentees": session.mentees.all(),
                        "mentors": session.mentors.all(),
                        "session_time": session.slot.time,
                    }
                )

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

        sessions = MentorshipSession.objects.filter(finalized=False)
        for session in sorted(sessions, key=lambda x: x.slot.time):
            if session.slot.time < (datetime.datetime.now() + datetime.timedelta(hours=36)):
                session.delete()

        for mentee in MentorshipMentee.objects.filter(responded=True):
            if mentee.potential_sessions_as_mentee.count() == 0 and mentee.assigned_sessions_as_mentee.count() == 0:
                unpaired.append(mentee)

        for unpaired_mentee in unpaired:
            send_email_message(
                "scheduling_failed",
                from_="pycon-mentorship@python.org",
                to=[str(unpaired_mentee)],
                context={
                    "mentorship_signup_link": "https://us.pycon.org/2019/mentorship/form/",
                }
            )
