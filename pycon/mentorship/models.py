import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class MentorshipSlot(models.Model):
    time = models.DateTimeField(auto_now=False, null=False)

    def available_mentors(self):
        return [x.mentor for x in MentorshipAvailability.objects.filter(slot=self).all() if x.mentor.available]

    def __unicode__(self):
        return self.time.strftime('%b %d - %I %p')

class MentorshipMentor(models.Model):
    user = models.ForeignKey(User, related_name="mentorship_mentor", verbose_name="mentor", null=False)
    availability = models.IntegerField(default=1)

    @property
    def assigned_sessions_as_mentor(self):
        try:
            return self.mentorship_mentor_sessions.filter(finalized=True)
        except ValueError:
            return []

    @property
    def potential_sessions_as_mentor(self):
        try:
            return self.mentorship_mentor_sessions.filter(finalized=False)
        except ValueError:
            return []

    @property
    def available(self):
        return len(self.assigned_sessions_as_mentor) < self.availability

    def available_at(self, slot_time):
        try:
            slot_before = MentorshipSlot.objects.get(time=slot_time - datetime.timedelta(hours=1))
        except ObjectDoesNotExist:
            slot_before = None

        try:
            slot_after = MentorshipSlot.objects.get(time=slot_time + datetime.timedelta(hours=1))
        except ObjectDoesNotExist:
            slot_after = None

        try:
            slot = MentorshipSlot.objects.get(time=slot_time)
        except ObjectDoesNotExist:
            return False

        # Check to see if Mentor said they were available at the time
        try:
            self.mentorship_availability.get(slot=slot)
        except ObjectDoesNotExist:
            return False

        # Check to see if Mentor is already scheduled at the time or the slot before/after
        try:
            if slot_before is not None:
                try:
                    self.mentorship_mentor_sessions.get(slot=slot_before, finalized=True)
                    return False
                except ObjectDoesNotExist:
                    pass
            self.mentorship_mentor_sessions.get(slot=slot, finalized=True)
            return False
            if slot_after is not None:
                try:
                    self.mentorship_mentor_sessions.get(slot=slot_after, finalized=True)
                    return False
                except ObjectDoesNotExist:
                    pass
        except ObjectDoesNotExist:
            pass

        # Return based on if the Mentor has reached their max sessions
        return self.available

    def __unicode__(self):
        return self.user.email

class MentorshipMentee(models.Model):
    user = models.ForeignKey(User, related_name="mentorship_mentee", verbose_name="mentee", null=False)
    eligibility = models.IntegerField(default=1)
    responded = models.BooleanField(default=False)

    @property
    def assigned_sessions_as_mentee(self):
        try:
            return self.mentorship_mentee_sessions.filter(finalized=True)
        except ValueError:
            return []

    @property
    def potential_sessions_as_mentee(self):
        try:
            return self.mentorship_mentee_sessions.filter(finalized=False)
        except ValueError:
            return []

    @property
    def eligible(self):
        return len(self.assigned_sessions_as_mentee) < self.eligibility

    def __unicode__(self):
        return self.user.email

class MentorshipAvailability(models.Model):
    mentor = models.ForeignKey(MentorshipMentor, related_name="mentorship_availability", verbose_name="mentorship availability")
    slot = models.ForeignKey(MentorshipSlot, related_name="mentorship_availability", verbose_name="mentorship slot")

    def slot_time(self):
        return self.slot.time

    def viable(self):
        return self.mentor.available

    viable.boolean = True

    slot_time.admin_order_field = 'slot__time'

    def __unicode__(self):
        return "%s - %s" % (str(self.mentor), str(self.slot.time))

class MentorshipSession(models.Model):
    slot = models.ForeignKey(MentorshipSlot, related_name="mentorship_session", verbose_name="mentorship slot")
    finalized = models.BooleanField(default=False)
    mentors = models.ManyToManyField(MentorshipMentor, related_name="mentorship_mentor_sessions")
    mentees = models.ManyToManyField(MentorshipMentee, related_name="mentorship_mentee_sessions")

    def slot_time(self):
        return self.slot.time

    def available_mentors(self):
        slot_mentors = self.slot.available_mentors()
        for mentor in self.mentors.all():
            slot_mentors = filter(lambda a: a != mentor, slot_mentors)
        return slot_mentors

    slot_time.admin_order_field = 'slot__time'

    def finalize(self):
        self.finalized = True
        self.save()
        for mentee in self.mentees.all():
            for session in mentee.potential_sessions_as_mentee:
                if session == self:
                    continue
                session.mentees.remove(mentee)
        for mentor in self.mentors.all():
            for session in mentor.potential_sessions_as_mentor:
                if session == self:
                    continue
                if not mentor.available_at(session.slot.time):
                    session.mentors.remove(mentor)
                session.slot.mentorship_availability.filter(mentor=mentor).delete()

    @property
    def mentors_count(self):
        return self.mentors.count()

    @property
    def mentees_count(self):
        return self.mentees.count()

    def __unicode__(self):
        return 'Mentorship Session'

def generate_availabile_slots():
    slots = []
    for slot in MentorshipSlot.objects.filter(time__gt=(datetime.datetime.now() + datetime.timedelta(hours=36))):
        mentors = []
        for ma in slot.mentorship_availability.all():
            if ma.mentor.available_at(slot.time) and ma.mentor.available:
                mentors.append(ma.mentor)
        if len(mentors) > 1:
            slots.append(slot)

    return sorted(slots, key=lambda x: x.time)
