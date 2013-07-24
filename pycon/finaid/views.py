from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from .forms import FinancialAidApplicationForm, MessageForm
from .models import FinancialAidApplication, FinancialAidMessage
from .utils import applications_open,  email_address, has_application, \
    is_reviewer, send_email_message


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

        # Let user know we got it by emailing them
        template_name = "application_" + \
                        ("submitted" if applying else "edited")
        send_email_message(template_name,
                           from_=email_address(),
                           to=[request.user.email],
                           context={})

        # Also display a message to them
        messages.add_message(request, messages.INFO,
                             _(u"Application submitted"))

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
    """
    Show an applicant the status of their application.
    Allow them to see messages from the reviewers and to submit
    messages to them.
    """
    if not has_application(request.user):
        messages.add_message(request, messages.ERROR,
                             _(u'You have not applied for financial aid'))
        return redirect("dashboard")

    if request.method == 'POST':
        message = FinancialAidMessage(user=request.user,
                                      application=request.user.financial_aid,
                                      visible=True)
        message_form = MessageForm(request.POST, instance=message)
        if message_form.is_valid():
            message = message_form.save()

            # Send notice to the reviewers/pycon-aid alias
            # (applicant submitted this message so no need to tell them)
            context = {
                'user': request.user,
                'message': message,
                # FIXME: Add link where reviewer can look at the application
            }
            send_email_message("applicant_message",
                               from_=request.user.email,
                               to=[email_address()],
                               context=context)

            return redirect(request.path)
    else:
        message_form = MessageForm()

    # Only show the applicant messages that are supposed to be visible to the
    # applicant
    visible_messages = FinancialAidMessage.objects.filter(
        application=request.user.financial_aid,
        visible=True
    )

    return render(request, "finaid/status.html", {
        'application': request.user.financial_aid,
        'visible_messages': visible_messages,
        'form': message_form,
    })
