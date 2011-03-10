from django.contrib.auth.models import Group, User

from schedule.models import Presentation, SessionRole


# @@@ Would probably be a good idea to consolidate the
# accepted speaker functions


def accepted_speakers():
    speakers = set()
    for presentation in Presentation.objects.select_related("speaker__user"):
        for speaker in presentation.speakers():
            if speaker is not None and speaker.user is not None:
                speakers.add(speaker.user)
    return iter(speakers)


def accepted_talk_speakers():
    speakers = set()
    talks = Presentation.objects.filter(presentation_type=Presentation.PRESENTATION_TYPE_TALK)
    
    for presentation in talks.select_related("speaker__user"):
        for speaker in presentation.speakers():
            if speaker is not None and speaker.user is not None:
                speakers.add(speaker.user)
    return iter(speakers)


def accepted_panel_speakers():
    speakers = set()
    panels = Presentation.objects.filter(presentation_type=Presentation.PRESENTATION_TYPE_PANEL)
    
    for presentation in panels.select_related("speaker__user"):
        for speaker in presentation.speakers():
            if speaker is not None and speaker.user is not None:
                speakers.add(speaker.user)
    return iter(speakers)


def accepted_tutorial_speakers():
    speakers = set()
    panels = Presentation.objects.filter(presentation_type=Presentation.PRESENTATION_TYPE_TUTORIAL)
    
    for presentation in panels.select_related("speaker__user"):
        for speaker in presentation.speakers():
            if speaker is not None and speaker.user is not None:
                speakers.add(speaker.user)
    return iter(speakers)


def organizers():
    for user in User.objects.filter(is_staff=True):
        yield user


def reviewers():
    for user in Group.objects.get(name="reviewers").user_set.all():
        yield user


def reviewers_tutorial():
    for user in Group.objects.get(name="reviewers-tutorial").user_set.all():
        yield user


def session_staff():
    staff = set()
    for role in SessionRole.objects.select_related("user"):
        staff.add(role.user)
    return iter(staff)


def fivesixsix():
    for user in User.objects.filter(username__in=["brosner", "jtauber"]):
        yield user

# @@@ move to settings.py and accept dotted paths
user_lists = [
    accepted_speakers,
    accepted_talk_speakers,
    accepted_panel_speakers,
    accepted_tutorial_speakers,
    organizers,
    reviewers,
    reviewers_tutorial,
    fivesixsix,
    session_staff,
]
user_lists = dict([(f.__name__, f) for f in user_lists])