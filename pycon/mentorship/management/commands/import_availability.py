import argparse
import json

import dateutil

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from pycon.mentorship.models import MentorshipMentor
from pycon.mentorship.models import MentorshipSlot
from pycon.mentorship.models import MentorshipAvailability


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("mentor_availability", type=argparse.FileType("r"))

    def handle(self, *args, **options):
        input_file = options["mentor_availability"]
        mentorship_availability = json.loads(input_file.read())
        mentors_not_found = set()
        User = get_user_model()
        for slot, mentors in mentorship_availability.items():
            mentorship_slot, _ = MentorshipSlot.objects.get_or_create(time=slot)
            for mentor in mentors:
                try:
                    mentor_user = User.objects.get(email=mentor)
                    if mentor_user.speaker_profile.interested_mentor != '':
                        mentor_obj, _ = MentorshipMentor.objects.get_or_create(user=mentor_user)
                        mentorship_availability, _ = MentorshipAvailability.objects.get_or_create(mentor=mentor_obj, slot=mentorship_slot)
                except User.DoesNotExist:
                    mentors_not_found.add(mentor)
        print(mentors_not_found)
