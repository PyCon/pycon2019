import os
import shutil
from StringIO import StringIO
from uuid import uuid4
from zipfile import ZipFile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext

from pycon.models import ScheduledEvent, PyConStartupRowApplication, PyConRoomSharingRequest, PyConRoomSharingOffer
from pycon.forms import PyConStartupRowApplicationForm, PyConRoomSharingRequestForm, PyConRoomSharingOfferForm
from pycon.program_export import export


def program_export(request):
    folder = '/tmp/{0}/'.format(uuid4())
    try:
        export(folder)
        s = StringIO()
        z = ZipFile(s, "w")
        for dirpath, dirs, files in os.walk(folder):
            for f in files:
                fn = os.path.join(dirpath, f)
                z.write(fn, "program_export/" + fn.split(folder, 1)[1])
        z.close()
        response = HttpResponse(s.getvalue(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename=program_export.zip'
        return response
    finally:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except OSError:
                pass


def scheduled_event(request, slug):
    """Scheduled event detail page"""
    event = get_object_or_404(ScheduledEvent, slug=slug, published=True)
    return render(request, "scheduled_event.html", {
        'event': event,
        'page': {
            'title': event.name,
        }
    })


def scheduled_event_overview(request):
   """Overview of all ScheduledEvents"""
   events = ScheduledEvent.objects.filter(published=True).order_by('start').all()
   return render(request, "scheduled_event_overview.html", {
       'events': events,
   })


@login_required
def startuprow_apply(request):
    try:
        application = request.user.startuprow_application
    except PyConStartupRowApplication.DoesNotExist:
        application = None
    if request.method == "POST":
        if application:
            form = PyConStartupRowApplicationForm(request.POST, request.FILES, user=request.user, instance=application)
        else:
            form = PyConStartupRowApplicationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            if application and application.accepted:
                messages.warning(request, "Your PyCon Startup Row application cannot be edited once accepted!")
                return redirect("startuprow_apply")
            form.save()
            messages.success(request, "Your PyCon Startup Row application has been submitted!")
            return redirect("startuprow_apply")
    else:
        if application:
            form = PyConStartupRowApplicationForm(user=request.user, instance=application)
        else:
            form = PyConStartupRowApplicationForm(user=request.user)

    return render_to_response("startuprow/application.html", {
        "form": form,
    }, context_instance=RequestContext(request))

def room_sharing(request):
    return render(request, "room_sharing.html", {
        'room_sharing_offers': PyConRoomSharingOffer.objects.filter(approved=True).all(),
        'room_sharing_requests': PyConRoomSharingRequest.objects.filter(approved=True).all(),
    })

@login_required
def room_sharing_offer(request):
    try:
        room_sharing_offer = request.user.room_sharing_offer
    except PyConRoomSharingOffer.DoesNotExist:
        room_sharing_offer = None

    if request.method == "POST":
        if room_sharing_offer:
            form = PyConRoomSharingOfferForm(request.POST, request.FILES, user=request.user, instance=room_sharing_offer)
        else:
            form = PyConRoomSharingOfferForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your PyCon Room Sharing Offer has been submitted! It will be published after review.")
            return redirect("dashboard")
    else:
        if room_sharing_offer:
            form = PyConRoomSharingOfferForm(user=request.user, instance=room_sharing_offer)
        else:
            form = PyConRoomSharingOfferForm(user=request.user)

    return render_to_response("room_sharing/offer.html", {"form": form}, context_instance=RequestContext(request))

@login_required
def withdraw_room_sharing_offer(request):
    try:
        room_sharing_offer = request.user.room_sharing_offer
        room_sharing_offer.delete()
        messages.success(request, "Room Sharing Offer withdrawn")
        return redirect("dashboard")
    except PyConRoomSharingOffer.DoesNotExist:
        messages.warning('No Room Sharing Offer to withdraw')


@login_required
def room_sharing_request(request):
    try:
        room_sharing_request = request.user.room_sharing_request
    except PyConRoomSharingRequest.DoesNotExist:
        room_sharing_request = None

    if request.method == "POST":
        if room_sharing_request:
            form = PyConRoomSharingRequestForm(request.POST, request.FILES, user=request.user, instance=room_sharing_request)
        else:
            form = PyConRoomSharingRequestForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your PyCon Room Sharing Request has been submitted! It will be published after review.")
            return redirect("dashboard")
    else:
        if room_sharing_request:
            form = PyConRoomSharingRequestForm(user=request.user, instance=room_sharing_request)
        else:
            form = PyConRoomSharingRequestForm(user=request.user)

    return render_to_response("room_sharing/request.html", {"form": form}, context_instance=RequestContext(request))

@login_required
def withdraw_room_sharing_request(request):
    try:
        room_sharing_request = request.user.room_sharing_request
        room_sharing_request.delete()
        messages.success(request, "Room Sharing Request withdrawn")
        return redirect("dashboard")
    except PyConRoomSharingRequest.DoesNotExist:
        messages.warning('No Room Sharing Request to withdraw')
