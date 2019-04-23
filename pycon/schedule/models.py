import os
from datetime import datetime

from django.db import models

from django.contrib.auth.models import User

from symposion.schedule.models import Day, Slot, Presentation


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

    @property
    def needs_volunteers(self):
        has_chair = False
        has_runner = False
        for role in self.session_roles.all():
            if not has_chair:
                has_chair = (role.role == 1)
            if not has_runner:
                has_runner = (role.role == 2)
        return not (has_chair and has_runner)

class SessionRole(models.Model):

    SESSION_ROLE_CHAIR = 1
    SESSION_ROLE_RUNNER = 2

    SESSION_ROLE_TYPES = [
        (SESSION_ROLE_CHAIR, "Session Chair"),
        (SESSION_ROLE_RUNNER, "Session Runner"),
    ]

    session = models.ForeignKey(Session, related_name="session_roles")
    user = models.ForeignKey(User)
    role = models.IntegerField(choices=SESSION_ROLE_TYPES)
    status = models.NullBooleanField()

    submitted = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = [("session", "user", "role")]

    def __unicode__(self):
        return u"%s %s: %s" % (self.user, self.session,
                               self.SESSION_ROLE_TYPES[self.role-1][1])


def get_presentation_upload_path(instance, filename):
    return os.path.join(
        "presentation_slides/{}/{}/{}".format(
            instance.presentation.id,
            datetime.now().isoformat(),
            filename
        )
    )


class SlidesUpload(models.Model):
    presentation = models.ForeignKey(Presentation)
    slides = models.FileField(
        "PDF export of your slides",
        blank=False,
        null=False,
        upload_to=get_presentation_upload_path,
    )

    def filename(self):
        return os.path.basename(self.slides.name)
