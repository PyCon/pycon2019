from itertools import groupby
from operator import attrgetter

from django import template

from symposion.conference.models import current_conference

from ..models import Sponsor, SponsorLevel


register = template.Library()


@register.assignment_tag(name="sponsors")
def _sponsors(level=None):
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


@register.assignment_tag
def job_sponsors():
    """
    Returns active sponsors, grouped by level name, who have the job listing
    benefit.
    """
    conference = current_conference()
    sponsors = Sponsor.objects.filter(level__conference=conference, active=True)
    sponsors = sponsors.order_by('level__order', 'added')
    sponsors = [s for s in sponsors if s.joblisting_text]
    grouped_sponsors = groupby(sponsors, attrgetter('level.name'))
    grouped_sponsors = [(name, list(sponsors)) for name, sponsors in grouped_sponsors]
    return grouped_sponsors


@register.assignment_tag
def job_fair_participants():
    """
    Returns active sponsors and table number, grouped by level name, who will
    be participating in the Job Fair.
    """
    conference = current_conference()
    sponsors = Sponsor.objects.filter(level__conference=conference, active=True)
    sponsors = sponsors.order_by('level__order', 'added')
    sponsors = [s for s in sponsors if s.job_fair_participant]
    grouped_sponsors = groupby(sponsors, attrgetter('level.name'))
    grouped_sponsors = [(name, list(sponsors)) for name, sponsors in grouped_sponsors]
    return grouped_sponsors


@register.filter
def mod(a, b):
    return int(a) % int(b)
