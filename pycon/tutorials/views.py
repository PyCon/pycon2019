import logging

from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext as _

from symposion.schedule.models import Presentation

from pycon.models import PyConTutorialProposal

from .forms import BulkEmailForm, TutorialMessageForm
from .models import PyConTutorialMessage
from .utils import email_context, send_email_message, is_attendee_or_speaker


log = logging.getLogger(__name__)


@login_required
def tutorial_email(request, pk, pks):
    presentation = get_object_or_404(Presentation, pk=pk)

    if not request.user.is_staff:
        if not is_attendee_or_speaker(request.user, presentation):
            return HttpResponseForbidden(_(u"Not authorized for this page"))

    pks = pks.split(",")
    user_model = get_user_model()
    recipients = user_model.objects.filter(pk__in=pks)
    emails = recipients.values_list('email', flat=True)

    from_speaker = False
    if hasattr(request.user, 'speaker_profile'):
        from_speaker = request.user.speaker_profile in presentation.speakers()

    form = BulkEmailForm()
    if request.method == 'POST':
        form = BulkEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            context = email_context(
                request,
                presentation.proposal,
                body,
                subject=subject)
            try:
                # Send Email to each recipient separately,
                send_email_message("direct_email",
                                   from_=settings.DEFAULT_FROM_EMAIL,
                                   to=[],
                                   bcc=emails,
                                   context=context,
                                   headers={'Reply-To': request.user.email})
            except SMTPException:
                log.exception("ERROR sending Tutorial emails")
                messages.add_message(request, messages.ERROR,
                                     _(u"There was some error sending emails, "
                                       u"not all of them might have made it"))
            else:
                messages.add_message(request, messages.INFO,
                                     _(u"Email(s) sent"))
            url = reverse(
                'schedule_presentation_detail',
                args=[presentation.pk]
            )
            return redirect(url)

    ctx = {
        'presentation': presentation,
        'form': form,
        'users': recipients,
        'from_speaker': from_speaker
    }

    return render(request, "tutorials/email.html", ctx)


@login_required
def tutorial_message(request, pk):

    tutorial = get_object_or_404(PyConTutorialProposal, pk=pk)
    presentation = Presentation.objects.get(proposal_base=tutorial)
    if not request.user.is_staff:
        if not is_attendee_or_speaker(request.user, presentation):
            return HttpResponseForbidden(_(u"Not authorized for this page"))

    message_form = TutorialMessageForm()
    if request.method == 'POST':
        message = PyConTutorialMessage(user=request.user,
                                       tutorial=tutorial)
        message_form = TutorialMessageForm(request.POST, instance=message)
        if message_form.is_valid():
            message = message_form.save()
            context = email_context(request, tutorial, message)
            sender_email = request.user.email
            speakers = [x.email for x in tutorial.speakers()
                        if x.email != sender_email]
            attendees = [x.email for x in tutorial.registrants.all()
                         if x.email != sender_email]
            recipients = speakers + attendees

            # Send new message notice to speakers/attendees
            send_email_message("message",
                               from_=settings.DEFAULT_FROM_EMAIL,
                               to=[request.user.email],
                               bcc=recipients,
                               context=context)
        messages.add_message(request, messages.INFO, _(u"Message sent"))
        url = reverse('schedule_presentation_detail', args=[presentation.pk])
        return redirect(url)

    return render(request, "tutorials/message.html", {
        'presentation': presentation,
        'form': message_form
        })
