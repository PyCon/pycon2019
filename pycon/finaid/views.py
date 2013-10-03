import logging
import re

from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.template import Template, Context
from django.utils.translation import ugettext as _

from .forms import FinancialAidApplicationForm, MessageForm, \
    FinancialAidReviewForm, ReviewerMessageForm, BulkEmailForm
from .models import FinancialAidApplication, FinancialAidMessage, \
    FinancialAidReviewData
from .utils import applications_open, email_address, email_context, \
    has_application, is_reviewer, send_email_message


log = logging.getLogger(__name__)


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

        context = email_context(request, application)

        # Let user know we got it by emailing them
        # Also notify the committee
        template_name = "applicant/" + \
                        ("submitted" if applying else "edited")
        send_email_message(template_name,
                           from_=email_address(),
                           to=[request.user.email],
                           context=context)
        template_name = "reviewer/" + \
                        ("submitted" if applying else "edited")
        send_email_message(template_name,
                           from_=request.user.email,
                           to=[email_address()],
                           context=context)

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
    """Starting view for reviewers - list the applications"""
    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    if request.method == 'POST':
        # They want to do something to bulk applicants
        # Find the checkboxes they checked
        regex = re.compile(r'^finaid_application_(.*)$')
        pks = []
        for field_name in request.POST:
            m = regex.match(field_name)
            if m:
                pks.append(m.group(1))
        if not len(pks):
            messages.add_message(
                request, messages.ERROR,
                _(u"Please select at least one application"))
            return redirect(request.path)

        pks = ",".join(pks)
        if 'email_action' in request.POST:
            # They want to email applicants
            return redirect('finaid_email', pks=pks)
        if 'message_action' in request.POST:
            # They want to attach a message to applications
            return redirect('finaid_message', pks=pks)
        messages.add_message(request, messages.ERROR, "WHAT?")

    return render(request, "finaid/application_list.html", {
        "applications": FinancialAidApplication.objects.all(),
    })


@login_required
def finaid_message(request, pks):
    """Add a message to some applications"""
    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    pks = pks.split(",")
    applications = FinancialAidApplication.objects.filter(pk__in=pks)\
        .select_related('user')
    if not applications.exists():
        messages.add_message(request, messages.ERROR, _(u"No applications selected"))
        return redirect('finaid_review')

    if request.method == 'POST':
        for application in applications:
            message = FinancialAidMessage(user=request.user,
                                          application=application)
            message_form = ReviewerMessageForm(request.POST, instance=message)
            if message_form.is_valid():
                message = message_form.save()
                # Send notice to reviewers/pycon-aid alias, and the applicant if visible
                context = email_context(request, application, message)
                send_email_message("reviewer/message",
                                   # From whoever is logged in clicking the buttons
                                   from_=request.user.email,
                                   to=[email_address()],
                                   context=context)
                # If visible to applicant, notify them as well
                if message.visible:
                    send_email_message("applicant/message",
                                       from_=request.user.email,
                                       to=[application.user.email],
                                       context=context)
            messages.add_message(request, messages.INFO, _(u"Messages sent"))
        return redirect(reverse('finaid_review'))
    else:
        message_form = ReviewerMessageForm()

    return render(request, "finaid/reviewer_message.html", {
        'applications': applications,
        'form': message_form,
    })


@login_required
def finaid_email(request, pks):
    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    pks = pks.split(",")
    applications = FinancialAidApplication.objects.filter(pk__in=pks)\
        .select_related('user')
    emails = [app.user.email for app in applications]

    form = None
    if request.method == 'POST':
        form = BulkEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = email_address()
            template_text = form.cleaned_data['template'].template
            template = Template(template_text)
            # emails will be the datatuple arg to send_mail_mail
            emails = []
            for application in applications:
                try:
                    review = application.review
                except FinancialAidReviewData.DoesNotExist:
                    review = None

                ctx = {
                    'application': application,
                    'review': review,
                }
                text = template.render(Context(ctx))
                emails.append((subject, text, from_email,
                               [application.user.email]))
            try:
                send_mass_mail(emails)
            except SMTPException:
                log.exception("ERROR sending financial aid emails")
                messages.add_message(request, messages.ERROR,
                                     _(u"There was some error sending emails, "
                                       u"not all of them might have made it"))
            else:
                messages.add_message(request, messages.INFO, _(u"Emails sent"))
            return redirect(reverse('finaid_review'))

    ctx = {
        'form': form or BulkEmailForm(),
        'users': [app.user for app in applications]
    }
    return render(request, "finaid/email.html", ctx)


@login_required
def finaid_review_detail(request, pk):
    """Review a particular application"""
    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    application = get_object_or_404(FinancialAidApplication, pk=pk)

    try:
        review_data = application.review
    except FinancialAidReviewData.DoesNotExist:
        review_data = FinancialAidReviewData(application=application)

    message_form = None
    review_form = None

    if request.method == 'POST':
        if 'message_submit' in request.POST:
            message = FinancialAidMessage(user=request.user,
                                          application=application)
            message_form = ReviewerMessageForm(request.POST, instance=message)
            if message_form.is_valid():
                message = message_form.save()
                # Send notice to the reviewers alias
                # If the message is visible, also send to the applicant
                context = email_context(request, application, message)
                # Notify reviewers
                send_email_message("reviewer/message",
                                   from_=request.user.email,
                                   to=[email_address()],
                                   context=context)
                # If visible to applicant, notify them as well
                if message.visible:
                    send_email_message("applicant/message",
                                       from_=request.user.email,
                                       to=[application.user.email],
                                       context=context)
                messages.add_message(
                    request, messages.INFO,
                    _(u"Message has been added to the application, and recipients notified by email."))
                return redirect(request.path)
        elif 'review_submit' in request.POST:
            review_form = FinancialAidReviewForm(request.POST,
                                                 instance=review_data)
            if review_form.is_valid():
                review_data = review_form.save()
                return redirect(reverse("finaid_review"))
        else:
            log.error("finaid_review_detail posted with unknown form: %r"
                      % request.POST)
            return HttpResponseForbidden("HEY WHY WAS THIS POSTED")

    # Create initial forms if needed
    message_form = message_form or ReviewerMessageForm()
    review_form = review_form or FinancialAidReviewForm(instance=review_data)

    context = {
        "application": application,
        "message_form": message_form,
        "review_form": review_form,
        "review_messages": FinancialAidMessage.objects.filter(
            application=application
        )
    }
    return render(request, "finaid/review.html", context)


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
        application = request.user.financial_aid
        message = FinancialAidMessage(user=request.user,
                                      application=application,
                                      visible=True)
        message_form = MessageForm(request.POST, instance=message)
        if message_form.is_valid():
            message = message_form.save()

            # Send notice to the reviewers/pycon-aid alias
            # (applicant submitted this message so no need to tell them)
            context = email_context(request, application, message)
            send_email_message("reviewer/message",
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
