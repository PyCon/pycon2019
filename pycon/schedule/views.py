from collections import Callable, OrderedDict

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

from django.db.models import Max


from .models import Session, SessionRole, Presentation, SlidesUpload
from .forms import SlidesUploadForm
from pycon.pycon_api.decorators import api_view
from symposion.schedule.models import Slot


def session_list(request):
    sessions = Session.objects.all().order_by('pk')

    return render(request, "schedule/session_list.html", {
        "sessions": sessions,
    })


@login_required
def session_staff_email(request):

    if not request.user.is_staff:
        return redirect("schedule_session_list")

    data = "\n".join(user.email
                     for user in User.objects.filter(sessionrole__isnull=False).distinct())

    return HttpResponse(data, content_type="text/plain;charset=UTF-8")


def session_detail(request, session_id):

    session = get_object_or_404(Session, id=session_id)

    chair = None
    chair_denied = False
    chairs = SessionRole.objects.filter(
        session=session, role=SessionRole.SESSION_ROLE_CHAIR).exclude(status=False)
    if chairs:
        chair = chairs[0].user
    else:
        if request.user.is_authenticated():
            # did the current user previously try to apply and got rejected?
            if SessionRole.objects.filter(
                    session=session, user=request.user,
                    role=SessionRole.SESSION_ROLE_CHAIR, status=False):
                chair_denied = True

    runner = None
    runner_denied = False
    runners = SessionRole.objects.filter(
        session=session, role=SessionRole.SESSION_ROLE_RUNNER).exclude(status=False)
    if runners:
        runner = runners[0].user
    else:
        if request.user.is_authenticated():
            # did the current user previously try to apply and got rejected?
            if SessionRole.objects.filter(
                    session=session, user=request.user,
                    role=SessionRole.SESSION_ROLE_RUNNER, status=False):
                runner_denied = True

    if request.method == "POST" and request.user.is_authenticated():
        if not hasattr(request.user, "profile") or not request.user.profile.is_complete:
            response = redirect("profile_edit")
            response["Location"] += "?next=%s" % request.path
            return response

        role = request.POST.get("role")
        if role == "chair":
            if chair is None and not chair_denied:
                SessionRole(
                    session=session, role=SessionRole.SESSION_ROLE_CHAIR, user=request.user).save()
        elif role == "runner":
            if runner is None and not runner_denied:
                SessionRole(
                    session=session, role=SessionRole.SESSION_ROLE_RUNNER, user=request.user).save()
        elif role == "un-chair":
            if chair == request.user:
                session_role = SessionRole.objects.filter(
                    session=session, role=SessionRole.SESSION_ROLE_CHAIR, user=request.user)
                if session_role:
                    session_role[0].delete()
        elif role == "un-runner":
            if runner == request.user:
                session_role = SessionRole.objects.filter(
                    session=session, role=SessionRole.SESSION_ROLE_RUNNER, user=request.user)
                if session_role:
                    session_role[0].delete()

        return redirect("schedule_session_detail", session_id)

    return render(request, "schedule/session_detail.html", {
        "session": session,
        "chair": chair,
        "chair_denied": chair_denied,
        "runner": runner,
        "runner_denied": runner_denied,
    })


@api_view
def session_staff_json(request):
    """
    Return session runners and chairs in JSON format.

    Requires API Key.

    URL: /<YEAR>/schedule/session-staff.json

    The data returned is in JSON format, and looks like::

        {
            'code': 200,
            'data': [<slotdata>, <slotdata>, ..., <slotdata>]
        }

    where each `<slotdata>` looks like::

        {
            "conf_key": 123, // fk into conference.json
            "chair_name": "Jane Smith",
            "chair_email": "jane@smith.net"
            "runner_name": "John Doe",
            "runner_email": "john@doe.net"
        }

    The conf_key is the same as the conf_key returned for talks by the
    `schedule_json` API.
    """
    data = []
    for slot in Slot.objects.all().order_by("start"):
        for session in slot.sessions.all():
            item = {
                'conf_key': slot.pk
            }
            roles = session.sessionrole_set.exclude(status=False)

            chair = roles.filter(role=SessionRole.SESSION_ROLE_CHAIR).first()
            if chair:
                item['chair_name'] = chair.user.get_full_name()
                item['chair_email'] = chair.user.email
            else:
                item['chair_name'] = ""
                item['chair_email'] = ""

            runner = roles.filter(role=SessionRole.SESSION_ROLE_RUNNER).first()
            if runner:
                item['runner_name'] = runner.user.get_full_name()
                item['runner_email'] = runner.user.email
            else:
                item['runner_name'] = ""
                item['runner_email'] = ""
            data.append(item)

    return (data, 200)


@login_required
def slides_upload(request, presentation_id):
    presentation = Presentation.objects.get(pk=presentation_id)
    if request.user.speaker_profile != presentation.speaker and request.user.speaker not in presentation.additional_speakers:
        messages.add_message(request, messages.ERROR, "You are not a presenter for that presentation!")
        return redirect("dashboard")

    if request.method == 'POST':
        form = SlidesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.presentation = presentation
            form.save()
            messages.add_message(request, messages.INFO, "Thank you for uploading your slides!")
            return redirect("dashboard")
    else:
        form = SlidesUploadForm()
        return render(request, "pycon/schedule/slides_upload.html", {'form': form, 'presentation': presentation})


@login_required
@permission_required('pycon_schedule.can_download_slides', raise_exception=True)
def slides_download(request):

    """Build the slides download page for the captioners."""
    available_slides = SlidesUpload.objects.annotate(room=Max('presentation__slot__slotroom__room__name')).order_by(
        'presentation__slot__day__date',
        'room',
        'presentation__slot__start'
    )

    # Django ORM does ordering but not grouping, so build the nested display
    # order the hard way.
    day_room_time = OrderedDefaultdict(lambda : OrderedDefaultdict(list))
    for slide_upload in available_slides:
        day_room_time[_slides_date(slide_upload)][_slides_room(slide_upload)].append(slide_upload)

    # now that we accumulated all of the days/rooms, change back to non-default_dict, so templates work
    grouped_slides = OrderedDict()
    for day, rooms in day_room_time.items():
        grouped_slides[day] = OrderedDict(sorted(rooms.items(), key=lambda room: room[0]))
    return render(request, "pycon/schedule/slides_download.html", context={'grouped_slides': grouped_slides})


def _slides_date(slide_upload):
    """Extracted dict key creation for readability"""
    return slide_upload.presentation.slot.day.date


def _slides_room(slide_upload):
    """Extracted dict key creation for readability"""
    room = slide_upload.presentation.slot.rooms.first()
    if room is not None:
         return room.name
    return 'None'


class OrderedDefaultdict(OrderedDict):
    """ A defaultdict with OrderedDict as its base class. """

    def __init__(self, default_factory=None, *args, **kwargs):
        if not (default_factory is None
                or isinstance(default_factory, Callable)):
            raise TypeError('First argument must be callable or None.')
        super(OrderedDefaultdict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key,)
        self[key] = value = self.default_factory()
        return value
