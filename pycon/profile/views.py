from pprint import pformat
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import Profile
from .forms import ProfileForm


@login_required
def profile_edit(request):
    
    next = request.GET.get("next")
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
    )
    
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            messages.add_message(request, messages.SUCCESS,
                _("Successfully updated profile.")
            )
            if next:
                return redirect(next)
        else:
            return HttpResponse(
                status=400,
                content=pformat(form.errors).encode('utf-8')
            )
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, "profiles/edit.html", {
        "form": form,
        "next": next,
    })
