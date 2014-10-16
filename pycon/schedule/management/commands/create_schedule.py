import csv
import time

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from symposion.conference.models import Section, current_conference
from symposion.proposals.models import ProposalBase
from symposion.schedule.models import Day, Room, Schedule, SlotKind, Slot, SlotRoom


ROOM_KEY = 'Track'
DAY_KEY = 'Day'
START_KEY = 'Start Time'
DURATION_KEY = 'Duration'
PRESENTATION_ID_KEY = 'ID'

class Command(BaseCommand):

    def _get_start_end_times(self, data):
        "Return start and end time objects"
        start_time = time.strptime(data[START_KEY], '%I:%M %p')
        start = datetime(100, 1, 1, start_time.tm_hour, start_time.tm_min, 00)
        end = start + timedelta(minutes=int(data[DURATION_KEY]))
        return start.time(), end.time()

    def _build_rooms(self, schedule, data):
        "Get or Create Rooms based on schedule type and set of Tracks"
        # TODO: Ensure ordering...this isn't bulletproof for roman numerals, for example
        rooms = sorted(set([x[ROOM_KEY] for x in data]))
        for i, room in enumerate(rooms):
            name = '{0} {1}'.format(ROOM_KEY, room)
            room, _ = Room.objects.get_or_create(schedule=schedule, name=name, order=i)

    def _build_days(self, schedule, data):
        "Get or Create Days based on schedule type and set of Days"
        days = set([x[DAY_KEY] for x in data])
        for day in days:
            date = datetime.strptime(day, "%m/%d/%y")
            day, _ = Day.objects.get_or_create(schedule=schedule, date=date)

    def _build_lunches(self, schedule):
        "Get or Create Lunches for the Days and Rooms"

        slot_kind, _ = SlotKind.objects.get_or_create(label="Lunch", schedule=schedule)
        days = Day.objects.filter(schedule=schedule).order_by('date')[:2]
        rooms = Room.objects.filter(schedule=schedule).order_by('order')
        for day in days:
            for i, room in enumerate(rooms, start=1):
                if i % 2:
                    start = datetime(100, 1, 1, 12, 55, 00)
                else:
                    start = datetime(100, 1, 1, 12, 40, 00)
                end = start + timedelta(minutes=60)
                slot = Slot.objects.create(kind=slot_kind, day=day, start=start.time(), end=end.time())
                SlotRoom.objects.get_or_create(slot=slot, room=room)

    def _build_breaks(self, schedule):
        "Get or Create Breaks for the Days and Rooms"
        slot_kind, _ = SlotKind.objects.get_or_create(label="Break", schedule=schedule)
        days = Day.objects.filter(schedule=schedule).order_by('date')[:2]
        rooms = Room.objects.filter(schedule=schedule).order_by('order')
        for day in days:
            for i, room in enumerate(rooms, start=1):
                if i % 2:
                    start = datetime(100, 1, 1, 16, 00, 00)
                else:
                    start = datetime(100, 1, 1, 15, 45, 00)
                end = start + timedelta(minutes=30)
                slot = Slot.objects.create(kind=slot_kind, day=day, start=start.time(), end=end.time())
                SlotRoom.objects.get_or_create(slot=slot, room=room)

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("The first argument must be a Schedule Type (ex. Talk)" \
                " and the second argument a path/to/csv")
        else:
            section_name, path = args

        conf = current_conference()
        proposals = ProposalBase.objects.select_related("result").select_subclasses()
        # TODO: Pin start and end dates for the section?
        section, _ = Section.objects.get_or_create(name=section_name, conference=conf)
        schedule, _ = Schedule.objects.get_or_create(section=section)
        slot_kind, _ = SlotKind.objects.get_or_create(label=section_name.rstrip('s').lower(), schedule=schedule)

        with open(path, 'rb') as f:
            data = [x for x in csv.DictReader(f)]
            # build rooms
            self._build_rooms(schedule, data)
            # build_days
            self._build_days(schedule, data)
            self._build_lunches(schedule)
            self._build_breaks(schedule)
            # build Slot  -> SlotRoom -> Presentation associations
            for row in data:
                name = '{0} {1}'.format(ROOM_KEY, row[ROOM_KEY])
                room = Room.objects.get(schedule=schedule, name=name)
                date = datetime.strptime(row[DAY_KEY], "%m/%d/%y")
                day = Day.objects.get(schedule=schedule, date=date)
                start, end = self._get_start_end_times(row)
                slot = Slot.objects.create(kind=slot_kind, day=day, start=start, end=end)
                proposal = proposals.get(pk=row[PRESENTATION_ID_KEY])
                slot.assign(proposal.presentation)
                SlotRoom.objects.create(slot=slot, room=room)
