import bleach
import markdown

from django.conf import settings


def parse(text):
    """Convert markdown text to sanitized HTML."""
    text = markdown.markdown(text, extensions=["extra"], safe_mode=False)
    text = bleach.clean(text, tags=settings.BLEACH_ALLOWED_TAGS)
    return text
