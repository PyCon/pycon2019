import bleach

from django import template
from django.conf import settings

from symposion.reviews.models import Review, ReviewAssignment


register = template.Library()


@register.assignment_tag(takes_context=True)
def user_reviews(context):
    request = context["request"]
    reviews = Review.objects.filter(user=request.user)
    return reviews


@register.assignment_tag(takes_context=True)
def review_assignments(context):
    request = context["request"]
    assignments = ReviewAssignment.objects.filter(user=request.user)
    return assignments


@register.filter("bleach")
def _bleach(text):
    return bleach.clean(unicode(text), tags=settings.BLEACH_ALLOWED_TAGS)


def replace_prefix(text, find, replace):
    """Replace all leading instances of a string with another string.

    Args:
        text (str): Text to screw with
        find (str): Characters to replace
        replace (str): Characters to replace with

    Returns:
        str: `text` with all leading instances of `find` replaced with `replace`
    """
    leading_count = len(text) - len(text.lstrip(find))
    return replace*leading_count + text.lstrip(find)


def escape_indentation(text):
    """Replace leading tabs and spaces text input with appropriate encoded
    characters, spaces become '&nbsp;' and tabs become '&emsp;' Note that only
    initial spaces and tabs are encoded, you should apply this to each line
    of a multi-line string.

    Args:
        text (str): Text to screw with

    Returns:
        str: `text` with encoded characters in place of spaces and tabs
    """
    return replace_prefix(replace_prefix(text, "\t", "&emsp;"), " ", "&nbsp;")


@register.filter("indentation")
def _indentation(text):
    """Replace leading tabs and spaces on each line of text input with
    appropriate encoded characters, spaces become '&nbsp;' and tabs become
    '&emsp;'

    Args:
        text (str): Text to screw with

    Returns:
        str: `text` with encoded characters in place of spaces and tabs
    """
    return '\n'.join([escape_indentation(line) for line in text.split('\n')])
