from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import Template
from django.utils.translation import ugettext as _

from pycon.tutorials.forms import BulkEmailForm, TutorialMessageForm
from pycon.tutorials.models import PyConTutorialMessage
from pycon.tutorials.utils import email_context, send_email_message

from pycon.models import PyConTutorialProposal


@login_required
def tutorial_email(request, pks):

    pks = pks.split(",")
    user_model = get_user_model()
    attendees = user_model.objects.filter(pk__in=pks)
    emails = [user.email for user in attendees]

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
            # lookup PROPOSAL/TUTORIAL?
            return redirect(reverse('schedule_presentation_detail', pk=1))

    ctx = {
        'form': form or BulkEmailForm(),
        'users': [app.user for app in applications]
    }

    return render(request, "tutorial/email.html", ctx)


@login_required
def tutorial_message(request, pk):
    tutorial = get_object_or_404(PyConTutorialProposal, pk=pk)
    if request.method == 'POST':
        message = PyConTutorialMessage(user=request.user,
                                       tutorial=tutorial)
        message_form = TutorialMessageForm(request.POST, instance=message)
        if message_form.is_valid():
            message = message_form.save()
            context = email_context(request, tutorial, message)
            # Send notice to instructors
            import ipdb; ipdb.set_trace()
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
        url = reverse('schedule_presentation_detail', args=[tutorial.presentation.pk])
        return redirect(url)
    else:
        message_form = TutorialMessageForm()

    return render(request, "tutorials/tutorial_message.html", {
        'tutorial': tutorial,
        'form': message_form
        })
