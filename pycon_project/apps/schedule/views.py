from django.conf import settings
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from schedule.models import Event, Slot, Session


def schedule_list(request, template_name="schedule/schedule_list.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    event = get_object_or_404(Event, slug="djangocon-us-2010")
    slots = Slot.objects.filter(event=event).order_by("start")
    
    return render_to_response(template_name, dict({
        "event": event,
        "slots": slots,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))


def schedule_session(request, session_id, template_name="schedule/session_detail.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    session = Session.objects.get(id=session_id)
    
    return render_to_response(template_name, dict({
        "session": session,
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))