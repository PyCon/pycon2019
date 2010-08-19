from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.sites.models import Site

from mailer import send_html_mail


def send_email(to, kind, **kwargs):
    
    current_site = Site.objects.get_current()
    
    ctx = {
        "current_site": current_site,
        "STATIC_URL": settings.STATIC_URL,
    }
    ctx.update(kwargs.get("context", {}))
    subject = render_to_string("emails/%s/subject.txt" % kind, ctx)
    message_html = render_to_string("emails/%s/message.html" % kind, ctx)
    message_plaintext = strip_tags(message_html)
    
    from_email = settings.DEFAULT_FROM_EMAIL
    
    send_html_mail(subject, message_plaintext, message_html, from_email, to)
