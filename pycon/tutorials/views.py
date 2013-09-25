import logging

from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext as _

from symposion.schedule.models import Presentation

from pycon.models import PyConTutorialProposal

from .forms import BulkEmailForm, TutorialMessageForm
from .models import PyConTutorialMessage
from .utils import email_context, send_email_message


log = logging.getLogger(__name__)


@login_required
def tutorial_email(request, pk ,pks):
    presentation = get_object_or_404(Presentation, pk=pk)

    pks = pks.split(",")
    user_model = get_user_model()
    recipients = user_model.objects.filter(pk__in=pks)

    from_speaker = True if request.user in presentation.speakers() else False

    form = None
    if request.method == 'POST':
        form = BulkEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            # from instructor
            # BCC speakers
            from_email = request.user.email
            body = form.cleaned_data['body']
            # emails will be the datatuple arg to send_mail_mail
            emails = []
            for recip in recipients:
                ctx = {
                    'presentation': presentation,
                    'attendee': recip,
                }
                emails.append((subject, body, from_email,
                               [recip.email]))
            try:
                send_mass_mail(emails)
            except SMTPException:
                log.exception("ERROR sending Tutorial emails")
                messages.add_message(request, messages.ERROR,
                                     _(u"There was some error sending emails, "
                                       u"not all of them might have made it"))
            else:
                messages.add_message(request, messages.INFO, _(u"Email(s) sent"))
            url = reverse('schedule_presentation_detail', args=[presentation.pk])
            return redirect(url)

    ctx = {
        'presentation': presentation,
        'form': form or BulkEmailForm(),
        'users': recipients,
        'from_speaker': from_speaker
    }

    return render(request, "tutorials/email.html", ctx)


@login_required
def tutorial_message(request, pk):
    tutorial = get_object_or_404(PyConTutorialProposal, pk=pk)
    presentation = Presentation.objects.get(proposal_base=tutorial)

    if request.method == 'POST':
        message = PyConTutorialMessage(user=request.user,
                                       tutorial=tutorial)
        message_form = TutorialMessageForm(request.POST, instance=message)
        if message_form.is_valid():
            message = message_form.save()
            context = email_context(request, tutorial, message)
            # Send notice to instructors
            send_email_message("instructor/message",
                               from_=request.user.email,
                               to=[x.email for x in tutorial.speakers()],
                               context=context)
            # Send notice to attendees
            send_email_message("attendee/message",
                               from_=request.user.email,
                               to=[x.email for x in tutorial.registrants.all()],
                               context=context)
        messages.add_message(request, messages.INFO, _(u"Message sent"))
        url = reverse('schedule_presentation_detail', args=[presentation.pk])
        return redirect(url)
    else:
        message_form = TutorialMessageForm()

    return render(request, "tutorials/message.html", {
        'presentation': presentation,
        'form': message_form
        })
