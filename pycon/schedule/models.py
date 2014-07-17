from datetime import datetime

from django.db import models

from django.contrib.auth.models import User

from symposion.schedule.models import Day, Slot


class Session(models.Model):

    day = models.ForeignKey(Day, related_name="sessions")
    slots = models.ManyToManyField(Slot, related_name="sessions")

    def sorted_slots(self):
        return self.slots.order_by("start")

    def start(self):
        slots = self.sorted_slots()
        if slots:
            return list(slots)[0].start
        else:
            return None

    def end(self):
        slots = self.sorted_slots()
        if slots:
            return list(slots)[-1].end
        else:
            return None

    def __unicode__(self):
        start = self.start()
        end = self.end()
        if start and end:
            return "{}: {} - {}".format(
                self.day, start.strftime('%X'), end.strftime('%X'))
        return ""


class SessionRole(models.Model):

    SESSION_ROLE_CHAIR = 1
    SESSION_ROLE_RUNNER = 2

    SESSION_ROLE_TYPES = [
        (SESSION_ROLE_CHAIR, "Session Chair"),
        (SESSION_ROLE_RUNNER, "Session Runner"),
    ]

    session = models.ForeignKey(Session)
    user = models.ForeignKey(User)
    role = models.IntegerField(choices=SESSION_ROLE_TYPES)
    status = models.NullBooleanField()

    submitted = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = [("session", "user", "role")]

    def __unicode__(self):
        return u"%s %s: %s" % (self.user, self.session,
                               self.SESSION_ROLE_TYPES[self.role-1][1])
