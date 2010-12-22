from django.contrib.auth.models import Group, User

from schedule.models import Session


# @@@ Would probably be a good idea to consolidate the
# accepted speaker functions


def accepted_speakers():
    speakers = set()
    for session in Session.objects.select_related("speaker__user"):
        for speaker in session.speakers():
            if speaker is not None and speaker.user is not None:
                speakers.add(speaker.user)
    return iter(speakers)


def accepted_talk_speakers():
    speakers = set()
    talks = Session.objects.filter(session_type=Session.SESSION_TYPE_TALK)
    
    for session in talks.select_related("speaker__user"):
        for speaker in session.speakers():
            if speaker is not None and speaker.user is not None:
                speakers.add(speaker.user)
    return iter(speakers)


def accepted_panel_speakers():
    speakers = set()
    panels = Session.objects.filter(session_type=Session.SESSION_TYPE_PANEL)
    
    for session in panels.select_related("speaker__user"):
        for speaker in session.speakers():
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


# @@@ move to settings.py and accept dotted paths
user_lists = [
    accepted_speakers,
    accepted_talk_speakers,
    accepted_panel_speakers,
    organizers,
    reviewers,
    reviewers_tutorial,
]
user_lists = dict([(f.__name__, f) for f in user_lists])