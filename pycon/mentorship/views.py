from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from pycon.mentorship.models import generate_availabile_slots


@login_required
def mentorship_signup_view_slots(request):
     if request.user.speaker_profile.interested_mentee is not None:
         slots = generate_availabile_slots()
         timezone = request.user.account.timezone if request.user.account.timezone else 'US/Eastern'
         return render(request, "mentorship/mentorship_slots_view.html", {"slots": slots, "timezone": timezone})
     else:
         return Http404()
