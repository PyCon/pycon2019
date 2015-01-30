from django import template

from symposion.conference.models import current_conference

from ..models import Sponsor, SponsorLevel


register = template.Library()


@register.assignment_tag
def sponsors(level=None):
    """Return all active sponsors for this conference.

    Optionally limited to a specific level.
    """
    conference = current_conference()
    sponsors = Sponsor.objects.filter(level__conference=conference, active=True)
    if level:
        sponsors = sponsors.filter(level__name__iexact=level)
    sponsors = sponsors.order_by('level__order', 'added')
    return sponsors


@register.assignment_tag
def sponsor_levels():
    """Return all sponsorship levels for this conference."""
    conference = current_conference()
    return SponsorLevel.objects.filter(conference=conference)


@register.filter
def mod(a, b):
    return int(a) % int(b)
