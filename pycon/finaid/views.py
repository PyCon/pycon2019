import csv
import logging

from smtplib import SMTPException

import django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from .forms import FinancialAidApplicationForm, MessageForm, \
    FinancialAidReviewForm, ReviewerMessageForm, BulkEmailForm, ReceiptForm, \
    FinancialAidAcceptOfferForm, SpeakerGrantRequestForm
from .models import FinancialAidApplication, FinancialAidMessage, \
    FinancialAidReviewData, STATUS_CHOICES, STATUS_WITHDRAWN
from pycon.finaid.models import STATUS_SUBMITTED, STATUS_OFFERED, STATUS_ACCEPTED, STATUS_DECLINED, \
    STATUS_NEED_MORE, STATUS_INFO_NEEDED, APPLICATION_TYPE_SPEAKER, PYTHON_EXPERIENCE_INTERMEDIATE
from .utils import applications_open, email_context, \
    has_application, is_reviewer, send_email_message


log = logging.getLogger(__name__)

@login_required
def speaker_grant_edit(request):
    """Complete, or edit speaker grant request"""

    if has_application(request.user):
        application = request.user.financial_aid
        if application.status == STATUS_WITHDRAWN:
            applying = True
        else:
            applying = False
    else:
        application = FinancialAidApplication(user=request.user)
        applying = True

    application.application_type = APPLICATION_TYPE_SPEAKER
    application.presenting = 1
    application.profession = "" if application.profession is None else application.profession
    application.experience_level = PYTHON_EXPERIENCE_INTERMEDIATE if application.experience_level is None else application.experience_level
    application.what_you_want = "" if application.what_you_want is None else application.what_you_want

    form = SpeakerGrantRequestForm(request.POST or None,
                                   instance=application)

    if form.is_valid():
        application = form.save()
        if applying:
            application.set_status(STATUS_SUBMITTED, save=True)

        context = email_context(request, application)

        template_name = "reviewer/" + \
                        ("submitted" if applying else "edited")
        send_email_message(template_name,
                           from_=request.user.email,
                           to=[settings.FINANCIAL_AID_EMAIL],
                           context=context)

        # Also display a message to them
        messages.add_message(request, messages.INFO,
                             _(u"Speaker Grant Request completed"))

        return redirect("dashboard")

    return render(request, "finaid/speaker_edit.html", {
        "form": form,
        "applying": applying,
    })

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
        if application.status == STATUS_WITHDRAWN:
            applying = True
        else:
            applying = False
    else:
        application = FinancialAidApplication(user=request.user)
        applying = True

    form = FinancialAidApplicationForm(request.POST or None,
                                       instance=application)
    if form.is_valid():
        application = form.save()
        if applying:
            application.set_status(STATUS_SUBMITTED, save=True)

        context = email_context(request, application)

        # Let user know we got it by emailing them
        # Also notify the committee
        template_name = "applicant/" + \
                        ("submitted" if applying else "edited")
        send_email_message(template_name,
                           from_=settings.FINANCIAL_AID_EMAIL,
                           to=[request.user.email],
                           context=context)
        template_name = "reviewer/" + \
                        ("submitted" if applying else "edited")
        send_email_message(template_name,
                           from_=request.user.email,
                           to=[settings.FINANCIAL_AID_EMAIL],
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
        pk_list = request.POST.getlist('id')
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
                                   to=[settings.FINANCIAL_AID_EMAIL],
                                   context=context,
                                   headers={'Reply-To': settings.FINANCIAL_AID_EMAIL}
                                   )
                # If visible to applicant, notify them as well
                if message.visible:
                    send_email_message("applicant/message",
                                       from_=request.user.email,
                                       to=[application.user.email],
                                       context=context,
                                       headers={'Reply-To': settings.FINANCIAL_AID_EMAIL}
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
            subject_template = Template(form.cleaned_data['subject'])
            from_email = settings.FINANCIAL_AID_EMAIL
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
                    'name': application.user.get_full_name(),
                    'review': review,
                }
                text = template.render(Context(ctx))
                subject = subject_template.render(Context(ctx))
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
                                   to=[settings.FINANCIAL_AID_EMAIL],
                                   context=context)
                # If visible to applicant, notify them as well
                if message.visible:
                    send_email_message("applicant/message",
                                       from_=request.user.email,
                                       to=[application.user.email],
                                       context=context)
                messages.add_message(
                    request, messages.INFO,
                    _(u"Message has been added to the application, "
                      u"and recipients notified by email."))
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
                               to=[settings.FINANCIAL_AID_EMAIL],
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


def get_names_of_fields(model):
    if django.VERSION < (1, 8):
        # Old way, stops working in Django 1.8 (but new way doesn't work before Django 1.8)
        return [
            f.attname for f, __ in model._meta.get_fields_with_model()
        ]

    # https://docs.djangoproject.com/en/1.8/ref/models/meta/#migrating-from-the-old-api
    return [f.name for f in model._meta.get_fields()]


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AcceptDeclineWithdrawViewBase(LoginRequiredMixin, View):
    form = None

    def dispatch(self, request, *args, **kwargs):
        if not has_application(request.user):
            messages.add_message(request, messages.ERROR,
                                 _(u'You have not applied for financial aid'))
            return redirect("dashboard")
        if not self.status_okay(request):
            return redirect("dashboard")
        return super(AcceptDeclineWithdrawViewBase, self).dispatch(request, *args, **kwargs)

    def status_okay(self, request):
        if request.user.financial_aid.status != STATUS_OFFERED:
            messages.error(request, _(u"There is no pending offer of assistance."))
            return False
        return True

    def get(self, request, *args, **kwargs):
        application = request.user.financial_aid
        form_to_render = None
        if self.form is not None and application.review.amount > 0:
            form_to_render = self.form(
                request.POST or None,
                instance=application.review,
            )
        return render(request, "finaid/confirm.html", {
            'message': self.confirmation_message,
            'form': form_to_render,
        })

    def post(self, request, *args, **kwargs):
        application = request.user.financial_aid

        if self.form is not None and application.review.amount > 0:
            form = self.form(
                request.POST or None,
                instance=application.review,
            )
            if form.is_valid():
                application.review.save()
            else:
                return render(request, "finaid/confirm.html", {
                    'message': self.confirmation_message,
                    'form': form,
                })

        try:
            application.review
        except FinancialAidReviewData.DoesNotExist:
            FinancialAidReviewData(application=application)

        application.set_status(self.new_status)
        application.save()
        message = FinancialAidMessage.objects.create(
            user=request.user,
            application=application,
            visible=True,
            message=self.user_message,
        )
        context = email_context(request, application, message)
        send_email_message("reviewer/message",
                           from_=request.user.email,
                           to=[settings.FINANCIAL_AID_EMAIL],
                           context=context,
                           subject_template=self.staff_message_template,
                           )
        messages.info(request, self.user_message)
        return redirect("dashboard")


class FinaidAcceptView(AcceptDeclineWithdrawViewBase):
    confirmation_message = _("Do you want to accept the offer?")
    new_status = STATUS_ACCEPTED
    staff_message_template = \
        "{% load review_tags %}{{ user.get_full_name|bleach|safe }} " \
        "has accepted their financial aid offer"
    user_message = _("The offer has been accepted")
    form = FinancialAidAcceptOfferForm


class FinaidDeclineView(AcceptDeclineWithdrawViewBase):
    confirmation_message = _("Do you want to decline the offer?")
    new_status = STATUS_DECLINED
    staff_message_template = \
        "{% load review_tags %}{{ user.get_full_name|bleach|safe }} " \
        "has declined their financial aid offer"
    user_message = _("The offer has been declined")


class FinaidWithdrawView(AcceptDeclineWithdrawViewBase):
    confirmation_message = _("Do you want to withdraw your application?")
    new_status = STATUS_WITHDRAWN
    staff_message_template = \
        "{% load review_tags %}{{ user.get_full_name|bleach|safe }} " \
        "has withdrawn their financial aid application"
    user_message = _("The application has been withdrawn")

    def status_okay(self, request):
        if request.user.financial_aid.status == STATUS_WITHDRAWN:
            messages.error(request, _(u"The application has already been withdrawn"))
            return False
        return True


class SendFinaidMessageViewBase(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not has_application(request.user):
            messages.add_message(request, messages.ERROR,
                                 _(u'You have not applied for financial aid'))
            return redirect("dashboard")
        if not self.status_okay(request):
            return redirect("dashboard")
        return super(SendFinaidMessageViewBase, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
            send_email_message(self.email_template,
                               from_=request.user.email,
                               to=[settings.FINANCIAL_AID_EMAIL],
                               context=context)

            application.set_status(self.new_status)
            application.save()

            return redirect('dashboard')
        return render(request, self.template, {
            'form': message_form,
        })

    def get(self, request, *args, **kwargs):
        message_form = MessageForm()
        return render(request, self.template, {
            'form': message_form,
        })


class FinaidProvideInfoView(SendFinaidMessageViewBase):
    email_template = "applicant/provide_info"
    template = "finaid/provide_info.html"
    new_status = STATUS_SUBMITTED

    def status_okay(self, request):
        if request.user.financial_aid.status != STATUS_INFO_NEEDED:
            messages.error(request, _(u"There is no pending request for information."))
            return False
        return True


class FinaidRequestMoreView(SendFinaidMessageViewBase):
    email_template = "applicant/request_more"
    template = "finaid/request_more.html"
    new_status = STATUS_NEED_MORE

    def status_okay(self, request):
        if request.user.financial_aid.status != STATUS_OFFERED:
            messages.error(request, _(u"There is no pending offer of assistance."))
            return False
        return True


@login_required
def finaid_download_csv(request):
    # Download financial aid application data as a .CSV file

    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    # Fields to include
    application_field_names = ['id'] + [
        name for name in get_names_of_fields(FinancialAidApplication)
        if name not in ['id', 'review']
    ] + ['email', 'user']
    reviewdata_field_names = [
        name for name in get_names_of_fields(FinancialAidReviewData)
        if name not in ['application', 'id', 'last_update']
    ]

    # For these fields, use the get_FIELDNAME_display() method so we get
    # the name of the choice (or other custom string) instead of the internal value
    use_display_method = [
        'reimbursement_method',
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


def phyllis_finaid_download_csv(request):
    # Download financial aid application data as a .CSV file
    # Subset for Phyllis PyCon 2018
    #
    #  id
    #  user
    #  amount_requested
    #  presenting
    #  email
    #  status
    #  amount
    #  reimbursement_method
    #  legal_name
    #  address

    if not is_reviewer(request.user):
        return HttpResponseForbidden(_(u"Not authorized for this page"))

    # Fields to include
    application_field_names = [
        'id',
        'user',
        'amount_requested',
        'presenting',
        'email',
        'status',
    ]
    reviewdata_field_names = [
        'amount',
        'status',
        'reimbursement_method',
        'legal_name',
        'address',
    ]

    # For these fields, use the get_FIELDNAME_display() method so we get
    # the name of the choice (or other custom string) instead of the internal value
    use_display_method = [
        'reimbursement_method',
        'presenting',
        'status',
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
    response['Content-Disposition'] = 'attachment; filename="phyllis_financial_aid.csv"'

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
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.application = request.user.financial_aid
            form.save()

            # Display a message to user
            messages.add_message(request, messages.INFO,
                                 _(u"Receipt submitted"))
            return redirect("receipt_upload")

    else:
        form = ReceiptForm()

    receipts = request.user.financial_aid.receipts.all()
    return render(request, "finaid/receipt_upload.html", {
        'form': form,
        'receipts': receipts
    })
