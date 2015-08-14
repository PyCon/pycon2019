import json
import re

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from pycon.bulkemail.models import BulkEmail


def is_attendee_or_speaker(user, presentation):
    """
    Return True if the user is either a speaker or atendee.

    :param user: User instance
    :param presentation: Presentation instance
    """
    speakers = [x.user for x in presentation.speakers()]
    registrants = presentation.proposal.registrants.all()
    return user in speakers or user in registrants


def email_context(request, proposal, message=None, subject=None):
    """
    Return a dictionary with the context to be used when constructing
    email messages about this presentation from a template.
    """
    url = reverse(
        'schedule_presentation_detail',
        args=[proposal.presentation.pk]
    )
    presentation_url = request.build_absolute_uri(url)
    context = {
        'user': request.user,
        'message': message,
        'presentation': proposal.presentation,
        'presentation_url': presentation_url,
        'subject': subject
    }
    return context


def queue_email_message(template_name, from_, to, bcc, context, headers=None):
    """
    Send an email message.

    :param template_name: Use to construct the real template names for the
    subject and body like this: "tutorials/email/%(template_name)s/subject.txt"
    and "tutorials/email/%(template_name)s/body.txt"
    :param from_: From address to use
    :param to: List of addresses to send to
    :param bcc: List of addresses to send via bcc
    :param context: Dictionary with context to use when rendering the
    templates.
    :param headers: dict of optional, additional email headers
    """
    context = Context(context)

    name = "tutorials/email/%s/subject.txt" % template_name
    subject_template = get_template(name)
    subject = subject_template.render(context)
    # subjects must be a single line, no newlines
    # if there's a trailing newline, strip it; anything more than that,
    # let it fail (tests will fail) so we know the subject template is
    # not valid.
    subject = subject.rstrip(u"\n")

    name = "tutorials/email/%s/body.txt" % template_name
    body_template = get_template(name)
    body = body_template.render(context)

    # Important: By default, the MIME type of the body parameter in an
    # EmailMessage is "text/plain". That makes it safe to use "|safe" in
    # our email templates, and we do. If you change this to, say, send
    # HTML format email, you must go through the email templates and do
    # something better about escaping user data for safety.
    BulkEmail.objects.create(
        subject=subject,
        body=body,
        from_address=from_,
        to_addresses=to,
        bcc_addresses=bcc,
        headers=json.dumps(headers),
    )


def process_tutorial_request(request, presentation):
    """
        PyConTutorialProposals allow for additional communication methods
        between Instructor and attenddees.
    """
    if 'email_action' in request.POST:
        # Find the checkboxes they checked
        regex = re.compile(r'^user_(.*)$')
        pks = []
        for field_name in request.POST:
            m = regex.match(field_name)
            if m:
                pks.append(m.group(1))
        if not len(pks):
            messages.add_message(
                request, messages.ERROR,
                _(u"Please select at least one attendee"))
            return redirect(request.path)
        pks = ",".join(pks)
        return redirect('tutorial_email', pk=presentation.pk, pks=pks)

    if 'message_action' in request.POST:
        url = reverse(
            'tutorial_message',
            kwargs={"pk": presentation.proposal.pk}
        )
        return redirect(url)
    msg = _(u"An invalid form action was attempted")
    messages.add_message(request, messages.ERROR, msg)
    url = reverse('schedule_presentation_detail', args=[presentation.pk])
    return redirect(url)
