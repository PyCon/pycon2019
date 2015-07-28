import csv
import logging
import re

from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.template import Template, Context
from django.utils.translation import ugettext as _

from .forms import FinancialAidApplicationForm, MessageForm, \
    FinancialAidReviewForm, ReviewerMessageForm, BulkEmailForm, ReceiptForm
from .models import FinancialAidApplication, FinancialAidMessage, \
    FinancialAidReviewData, STATUS_CHOICES, Receipt
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
def finaid_review(request, pks=None):
    """Starting view for reviewers - list the applications"""
    # On a POST the pks are in the form.
    # On a GET there might be pks in the URL.

    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    if request.method == 'POST':
        # They want to do something to bulk applicants
        # Find the checkboxes they checked
        regex = re.compile(r'^finaid_application_(.*)$')
        pk_list = []
        for field_name in request.POST:
            m = regex.match(field_name)
            if m:
                pk_list.append(m.group(1))
        if not pk_list:
            messages.add_message(
                request, messages.ERROR,
                _(u"Please select at least one application"))
            return redirect(request.path)

        if 'email_action' in request.POST:
            # They want to email applicants
            pks = ",".join(pk_list)
            return redirect('finaid_email', pks=pks)
        elif 'message_action' in request.POST:
            # They want to attach a message to applications
            pks = ",".join(pk_list)
            return redirect('finaid_message', pks=pks)
        elif 'status_action' in request.POST:
            # They want to change applications' statuses
            applications = FinancialAidApplication.objects.filter(pk__in=pk_list)\
                .select_related('review')
            status = int(request.POST['status'])
            count = 0
            for application in applications:
                try:
                    review = application.review
                except FinancialAidReviewData.DoesNotExist:
                    review = FinancialAidReviewData(application=application)
                if review.status != status:
                    review.status = status
                    review.save()
                    count += 1
            messages.info(request,
                          "Updated %d application status%s" % (count, "" if count == 1 else "es"))
            pks = ",".join(pk_list)
            return redirect(reverse('finaid_review', kwargs=dict(pks=pks)))
        else:
            messages.error(request, "WHAT?")
    else:
        # GET - pks are in the URL.  maybe.
        pk_list = pks.split(",") if pks else []

    return render(request, "finaid/application_list.html", {
        "applications": FinancialAidApplication.objects.all().select_related('review'),
        "status_options": STATUS_CHOICES,
        "pks": [int(pk) for pk in pk_list],
    })


@login_required
def finaid_message(request, pks):
    """Add a message to some applications"""
    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    applications = FinancialAidApplication.objects.filter(pk__in=pks.split(","))\
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
                                   context=context,
                                   headers={'Reply-To': email_address()}
                                   )
                # If visible to applicant, notify them as well
                if message.visible:
                    send_email_message("applicant/message",
                                       from_=request.user.email,
                                       to=[application.user.email],
                                       context=context,
                                       headers={'Reply-To': email_address()}
                                       )
            messages.add_message(request, messages.INFO, _(u"Messages sent"))
        return redirect(reverse('finaid_review', kwargs=dict(pks=pks)))
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

    applications = FinancialAidApplication.objects.filter(pk__in=pks.split(","))\
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
            return redirect(reverse('finaid_review', kwargs=dict(pks=pks)))

    ctx = {
        'form': form or BulkEmailForm(),
        'users': [app.user for app in applications]
    }
    return render(request, "finaid/email.html", ctx)


@login_required
def finaid_review_detail(request, pk):
    """Review a particular application"""
    application = get_object_or_404(FinancialAidApplication, pk=pk)

    # Redirect a a reviewer who is attempting to access FA application detail
    # page to their edit page
    if is_reviewer(request.user) and request.user == application.user:
            return redirect("finaid_edit")

    if not is_reviewer(request.user):
        # Redirect a non reviewer to their FA edit page
        if has_application(request.user):
            return redirect("finaid_edit")
        return HttpResponseForbidden(_(u"Not authorized for this page"))

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


@login_required
def finaid_download_csv(request):
    # Download financial aid application data as a .CSV file

    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    # Fields to include
    application_field_names = ['id'] + [
        f.attname for f, model in FinancialAidApplication._meta.get_fields_with_model()
        if f.attname not in ['id', 'review']
    ] + ['email', 'user']
    reviewdata_field_names = [
        f.attname for f, model in FinancialAidReviewData._meta.get_fields_with_model()
        if f.attname not in ['application', 'id', 'last_update']
    ]

    # For these fields, use the get_FIELDNAME_display() method so we get
    # the name of the choice (or other custom string) instead of the internal value
    use_display_method = [
        'cash_check',
        'last_update',
        'presenting',
        'status',
        'travel_cash_check',
    ]

    def get_value(name, object):
        # Get a value from an application or review, using get_NAME_display
        # if appropriate, then forcing to a unicode string and encoding in
        # UTF-8 for CSV
        if name in use_display_method:
            display_method = getattr(object, "get_%s_display" % name)
            value = display_method()
        elif name == 'email':
            value = object.user.email
        else:
            value = getattr(object, name)
        return unicode(value).encode('utf-8')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financial_aid.csv"'

    writer = csv.DictWriter(
        response,
        fieldnames=application_field_names+reviewdata_field_names
    )
    writer.writeheader()

    default_review_data = FinancialAidReviewData()
    apps = FinancialAidApplication.objects.all().select_related('review')
    for application in apps.order_by('pk'):
        # They won't all have review data, so use the default values if they don't
        try:
            review = application.review
        except FinancialAidReviewData.DoesNotExist:
            review = default_review_data

        # Write the data for this application.
        data = {}
        for name in application_field_names:
            data[name] = get_value(name, application)
        for name in reviewdata_field_names:
            data[name] = get_value(name, review)
        writer.writerow(data)

    return response


@login_required
def receipt_upload(request):
    receipts = Receipt.objects.filter(user__username=request.user.username)

    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.user = request.user
            form.instance.application = request.user.financial_aid
            form.save()

            # Display a message to user
            messages.add_message(request, messages.INFO,
                                _(u"Receipt submitted"))

    else:
        form = ReceiptForm()
    return render(request, "finaid/receipt_upload.html", {
        'form': form,
        'receipts': receipts
    })


@login_required
def receipt_delete(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk).delete()
    return redirect("receipt_upload")
