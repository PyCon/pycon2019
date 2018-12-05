import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from pycon.mentorship.models import MentorshipSlot
from pycon.mentorship.models import MentorshipMentee
from pycon.mentorship.models import MentorshipSession
from pycon.mentorship.models import generate_availabile_slots


@login_required
def mentorship_view(request):
     timezone = request.user.account.timezone if request.user.account.timezone else 'US/Eastern'
     mentee, created = request.user.mentorship_mentee.get_or_create(user=request.user)
     if (not request.user.mentorship_mentee.get().eligible) or (len(request.user.mentorship_mentee.get().potential_sessions_as_mentee) > 0):
         return render(
             request, "mentorship/mentorship_signup_recieved.html",
             {
                 "potential_slots": request.user.mentorship_mentee.get().potential_sessions_as_mentee,
                 "assigned_slots": request.user.mentorship_mentee.get().assigned_sessions_as_mentee,
                 "timezone": timezone,
             }
         )
     # Short circuit out
     return render(request, "mentorship/mentorship_slots_full.html", {})
     if request.user.speaker_profile.interested_mentee != "":
         slots = generate_availabile_slots()
         if request.method == 'POST':

             errors = []
             selected_slots = []

             try:
                 selected_slots = [MentorshipSlot.objects.get(id=int(x)) for x in request.POST.getlist('slot_list')]
             except ObjectDoesNotExist:
                 errors.append(ValidationError(_("Invalid Slot selected"), 'invalid_slot'))

             if not all([s in slots for s in selected_slots]):
                 errors.append(ValidationError(_("Invalid Slot selected, it may have been scheduled already"), 'invalid_slot'))

             if len(selected_slots) > 3:
                 errors.append(ValidationError(_("Too many slots selected, limited to 3"), 'too_many_slots'))

             if errors:
                 return render(request, "mentorship/mentorship_slots_view.html", {"slots": slots, "timezone": timezone, "errors": errors})

             for slot in selected_slots:
                 session, created = MentorshipSession.objects.get_or_create(finalized=False, slot=slot)
                 for i in range(session.mentors.count(), 2):
                     mentors = slot.available_mentors()
                     session.mentors.add(mentors[random.randint(0, len(mentors)-1)])
                 mentee, created = MentorshipMentee.objects.get_or_create(user=request.user)
                 session.mentees.add(mentee)
                 session.save()
                 mentee.responded = True
                 mentee.save()

             return render(
                 request, "mentorship/mentorship_signup_recieved.html",
                 {
                     "potential_slots": request.user.mentorship_mentee.get().potential_sessions_as_mentee,
                     "assigned_slots": request.user.mentorship_mentee.get().assigned_sessions_as_mentee,
                     "timezone": timezone,
                 }
             )

         else:
             return render(request, "mentorship/mentorship_slots_view.html", {"slots": slots, "timezone": timezone})
     else:
         return Http404()
