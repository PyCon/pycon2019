from functools import wraps

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from sponsors.forms import SponsorApplicationForm, SponsorDetailsForm
from sponsors.models import Sponsor


def require_no_sponsorship(only_active=False):
    def inner(func):
        @wraps(func)
        def view(request, *args, **kwargs):
            if request.user.is_authenticated():
                try:
                    sponsorship = request.user.sponsorship
                except Sponsor.DoesNotExist:
                    pass
                else:
                    if not only_active or sponsorship.active:
                        return redirect(sponsorship)
            return func(request, *args, **kwargs)
        return view
    return inner


@require_no_sponsorship(only_active=True)
def sponsor_index(request):
    return render_to_response("sponsors/index.html", {
    }, context_instance=RequestContext(request))


@login_required
@require_no_sponsorship()
def sponsor_apply(request):
    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("sponsor_index")
    else:
        form = SponsorApplicationForm(user=request.user)
    return render_to_response("sponsors/apply.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if not sponsor.active or sponsor.applicant != request.user:
        return redirect("sponsor_index")

    if request.method == "POST":
        form = SponsorDetailsForm(request.POST, instance=sponsor)
        if form.is_valid():
            form.save()
            return redirect(request.path)
    else:
        form = SponsorDetailsForm(instance=sponsor)
    
    return render_to_response("sponsors/detail.html", {
        "sponsor": sponsor,
        "form": form,
    }, context_instance=RequestContext(request))
