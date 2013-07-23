from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

from .forms import FinancialAidApplicationForm
from .models import FinancialAidApplication
from .utils import is_reviewer, has_application, applications_open


@login_required
def finaid_edit(request):
    """Apply for, or edit application for, financial aid"""

    if not applications_open():
        messages.add_message(request, messages.ERROR,
                             _('Financial aid applications are not open '
                               'at this time'))
        return redirect("dashboard")

    if has_application(request.user):
        application = request.user.financial_aid
        applying = False
    else:
        application = FinancialAidApplication(user=request.user)
        applying = True

    form = FinancialAidApplicationForm(request.POST or None,
                                       instance=application)
    if form.is_valid():
        form.save()
        return redirect("dashboard")

    return render(request, "finaid/edit.html", {
        "form": form,
        "applying": applying,
    })


@login_required
def finaid_review(request):
    if not is_reviewer(request.user):
        return HttpResponseForbidden()
    raise NotImplementedError("financial aid reviewing not implemented yet")


@login_required
def finaid_status(request):
    if not has_application(request.user):
        messages.add_message(request, messages.ERROR,
                             _(u'You have not applied for financial aid'))
        return redirect("dashboard")

    return render(request, "finaid/status.html", {
        'application': request.user.financial_aid,
    })
