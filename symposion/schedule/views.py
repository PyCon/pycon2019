import json
import datetime

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader, Context

from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required

from pycon.tutorials.models import PyConTutorialProposal
from pycon.tutorials.utils import process_tutorial_request

from symposion.schedule.forms import SlotEditForm
from symposion.schedule.models import Schedule, Day, Slot, Presentation
from symposion.schedule.timetable import TimeTable


def fetch_schedule(slug):
    qs = Schedule.objects.all()

    if slug is None:
        if qs.count() > 1:
            raise Http404()
        schedule = next(iter(qs), None)
        if schedule is None:
            raise Http404()
    else:
        schedule = get_object_or_404(qs, section__slug=slug)

    return schedule


def schedule_conference(request):
    days = Day.objects.filter(schedule__published=True)
    days = days.select_related('schedule')
    days = days.prefetch_related('schedule__section')
    days = days.order_by('date')
    timetables = [TimeTable(day) for day in days]
    return render(request, "schedule/schedule_conference.html", {
        "timetables": timetables,
    })


def schedule_detail(request, slug=None):
    schedule = fetch_schedule(slug)
    if not schedule.published and not request.user.is_staff:
        raise Http404()

    days = Day.objects.filter(schedule=schedule)
    days = days.select_related('schedule')
    days = days.prefetch_related('schedule__section')
    days = days.order_by('date')
    timetables = [TimeTable(day) for day in days]

    return render(request, "schedule/schedule_detail.html", {
        "schedule": schedule,
        "timetables": timetables,
    })


def schedule_list(request, slug=None):
    schedule = fetch_schedule(slug)

    presentations = Presentation.objects.filter(section=schedule.section)
    presentations = presentations.exclude(cancelled=True)

    ctx = {
        "schedule": schedule,
        "presentations": presentations,
    }
    return render(request, "schedule/schedule_list.html", ctx)


def schedule_list_csv(request, slug=None):
    schedule = fetch_schedule(slug)

    presentations = Presentation.objects.filter(section=schedule.section)
    presentations = presentations.exclude(cancelled=True).order_by("id")

    response = HttpResponse(mimetype="text/csv")
    if slug:
        file_slug = slug
    else:
        file_slug = "presentations"
    response["Content-Disposition"] = 'attachment; filename="%s.csv"' % file_slug

    response.write(loader.get_template("schedule/schedule_list.csv").render(Context({
        "presentations": presentations,

    })))
    return response


@login_required
def schedule_edit(request, slug=None):
    if not request.user.is_staff:
        raise Http404()

    schedule = fetch_schedule(slug)

    days = Day.objects.filter(schedule=schedule)
    days = days.select_related('schedule')
    days = days.prefetch_related('schedule__section')
    days = days.order_by('date')
    timetables = [TimeTable(day) for day in days]

    return render(request, "schedule/schedule_edit.html", {
        "schedule": schedule,
        "timetables": timetables,
    })


@login_required
def schedule_slot_edit(request, slug, slot_pk):

    if not request.user.is_staff:
        raise Http404()

    slot = get_object_or_404(Slot, day__schedule__section__slug=slug, pk=slot_pk)

    if request.method == "POST":
        form = SlotEditForm(request.POST, slot=slot)
        if form.is_valid():
            save = False
            if "content_override" in form.cleaned_data:
                slot.content_override = form.cleaned_data["content_override"]
                save = True
            if "presentation" in form.cleaned_data:
                presentation = form.cleaned_data["presentation"]
                if presentation is None:
                    slot.unassign()
                else:
                    slot.assign(presentation)
            if save:
                slot.save()
        return redirect("schedule_edit", slug)
    else:
        form = SlotEditForm(slot=slot)
        ctx = {
            "slug": slug,
            "form": form,
            "slot": slot,
        }
        return render(request, "schedule/_slot_edit.html", ctx)


def schedule_presentation_detail(request, pk):

    presentation = get_object_or_404(Presentation, pk=pk)

    # Tutorials allow for communication between instructor/attendee(s).
    # Offload the logic to its utility
    if isinstance(presentation.proposal, PyConTutorialProposal) and \
            request.method == 'POST':
        return process_tutorial_request(request, presentation)

    if presentation.slot:
        schedule = presentation.slot.day.schedule
    else:
        schedule = None

    ctx = {
        "presentation": presentation,
        "proposal": presentation.proposal,
        "speakers": presentation.speakers,
        "schedule": schedule,
    }
    return render(request, "schedule/presentation_detail.html", ctx)


def json_serializer(obj):
    if isinstance(obj, datetime.time):
        return obj.strftime("%H:%M")
    raise TypeError


def schedule_json(request):
    slots = Slot.objects.all().order_by("start")
    data = []
    for slot in slots:
        if slot.kind.label in ["talk", "tutorial", "plenary"] and slot.content:
            slot_data = {
                "name": slot.content.title,
                "room": ", ".join(room["name"] for room in slot.rooms.values()),
                "start": slot.start_date.isoformat(),
                "end": slot.end_date.isoformat(),
                "duration": slot.duration,
                "authors": [s.name for s in slot.content.speakers()],
                "released": slot.content.proposal.recording_release,
                "license": "CC",
                "contact": [s.email for s in slot.content.speakers()],
                "abstract": getattr(slot.content.abstract, 'raw', slot.content.abstract),
                "description": getattr(slot.content.description, 'raw', slot.content.description),
                "conf_key": slot.pk,
                "conf_url": "https://%s%s" % (
                    Site.objects.get_current().domain,
                    reverse("schedule_presentation_detail", args=[slot.content.pk])
                ),
                "kind": slot.kind.label,
                "video_url": slot.content.video_url,
                "slides_url": slot.content.slides_url,
                "assets_url": slot.content.assets_url,
                "tags": "",
            }
        else:
            continue
        data.append(slot_data)

    for poster in Presentation.objects.filter(section__slug="posters", cancelled=False):
        poster_data = {
            "name": poster.title,
            "authors": [s.name for s in poster.speakers()],
            "description": getattr(poster.description, 'raw', poster.description),
            "abstract": getattr(poster.abstract, 'raw', poster.abstract),
            "license": "CC",
            "room": "Poster Room",
            "start": datetime.datetime(2014, 03, 17, 10).isoformat(),
            "end": datetime.datetime(2014, 03, 17, 13, 10).isoformat(),
            "contact": [s.email for s in poster.speakers()],
            "conf_key": 1000 + poster.pk,
            "conf_url": "https://%s%s" % (
                Site.objects.get_current().domain,
                reverse("schedule_presentation_detail", args=[poster.pk])
            ),
            "kind": "poster",
            "released": poster.proposal.recording_release,
        }
        data.append(poster_data)

    return HttpResponse(
        json.dumps(data, default=json_serializer),
        content_type="application/json"
    )
