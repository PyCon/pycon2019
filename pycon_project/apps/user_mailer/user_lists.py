from django.contrib.auth.models import Group, User

from schedule.models import Session


def accepted_speakers():
    speakers = set()
    for session in Session.objects.select_related("speaker__user"):
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

# @@@ move to settings.py and accept dotted paths
user_lists = [
    accepted_speakers,
    organizers,
    reviewers,
]
user_lists = dict([(f.__name__, f) for f in user_lists])