from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from proposals.models import Proposal
from review.models import ProposalResult
from schedule.models import Slot, Session


def schedule_list(request, template_name="schedule/schedule_list.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    slots = Slot.objects.all().order_by("start")
    
    return render_to_response(template_name, dict({
        "slots": slots,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_session(request, session_id, template_name="schedule/session_detail.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    session = get_object_or_404(Session, id=session_id)
    
    return render_to_response(template_name, dict({
        "session": session,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_list_talks(request):
    
    talks = Session.objects.filter(
        session_type__in=[Session.SESSION_TYPE_PANEL, Session.SESSION_TYPE_TALK]
    )
    talks = talks.order_by("pk")
    
    return render_to_response("schedule/list_talks.html", dict({
        "talks": talks,
    }), context_instance=RequestContext(request))


def schedule_list_tutorials(request):
    
    tutorials = Session.objects.filter(
        session_type=Session.SESSION_TYPE_TUTORIAL
    )
    tutorials = tutorials.order_by("pk")
    
    return render_to_response("schedule/list_tutorials.html", dict({
        "tutorials": tutorials,
    }), context_instance=RequestContext(request))


def schedule_list_posters(request):
    
    posters = Session.objects.filter(
        session_type=Session.SESSION_TYPE_POSTER
    )
    posters = posters.order_by("pk")
    
    return render_to_response("schedule/list_posters.html", dict({
        "posters": posters,
    }), context_instance=RequestContext(request))


def schedule_tutorials(request):
    
    tutorials = {
        "wed": {
            "morning": {
                "slot": Slot.objects.get(id=1),
                "sessions": Session.objects.filter(slot=1).order_by("pk"),
            },
            "afternoon": {
                "slot": Slot.objects.get(id=2),
                "sessions": Session.objects.filter(slot=2).order_by("pk"),
            }
        }, 
        "thurs": {
            "morning": {
                "slot": Slot.objects.get(id=3),
                "sessions": Session.objects.filter(slot=3).order_by("pk"),
            },
            "afternoon": {
                "slot": Slot.objects.get(id=4),
                "sessions": Session.objects.filter(slot=4).order_by("pk"),
            }
        }
    }
    
    ctx = {
        "tutorials": tutorials,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("schedule/tutorials.html", ctx)
