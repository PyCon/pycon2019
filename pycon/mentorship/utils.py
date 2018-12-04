from django.core.mail.message import EmailMessage
from django.template import Context, Template
from django.template.loader import get_template


def send_email_message(template_name, from_, to, context, headers=None, subject_template=None, bcc=True):
    """
    Send an email message.
    :param template_name: Use to construct the real template names for the
    subject and body like this: "finaid/email/%(template_name)s/subject.txt"
    and "finaid/email/%(template_name)s/body.txt"
    :param from_: From address to use
    :param to: List of addresses to send to
    :param context: Dictionary with context to use when rendering the
    templates.
    :param headers: dict of optional, additional email headers
    :param subject_template: optional string to use as the subject template, in place of
       mentorship/email/{{ template_name }}/subject.txt
    """
    context = Context(context)

    name = "mentorship/email/%s/subject.txt" % template_name
    if subject_template:
        subject_template = Template(subject_template)
    else:
        subject_template = get_template(name)
    subject = subject_template.render(context)
    subject = subject.rstrip(u"\n")

    name = "mentorship/email/%s/body.txt" % template_name
    body_template = get_template(name)
    body = body_template.render(context)

    if bcc:
        bcc_addresses = ['pycon-mentorship@python.org']
    else:
        bcc_addresses = []
    email = EmailMessage(subject, body, from_, to, bcc_addresses, reply_to=to, headers=headers)
    email.send()
