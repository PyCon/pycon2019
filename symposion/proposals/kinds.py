"""
Manage proposal kinds.

Everything is keyed off the ProposalKind slug value.
"""
from symposion.proposals.models import ProposalKind


class KindTracker(object):
    # Internal data structure
    def __init__(self, kind_slug):
        self.slug = kind_slug
        self.model_class = None
        self.form_class = None


trackers = {}
trackers_by_section_slug = {}


def _get_tracker(slug):
    if slug not in trackers:
        trackers[slug] = KindTracker(slug)
    return trackers[slug]


def register_proposal_model(kind_slug, model_class):
    _get_tracker(kind_slug).model_class = model_class


def register_proposal_form(kind_slug, form_class):
    _get_tracker(kind_slug).form_class = form_class


def get_proposal_model(kind_slug):
    model_class = _get_tracker(kind_slug).model_class
    if not model_class:
        raise ValueError("No model_class has been registered for proposal kind %r" % kind_slug)
    return model_class


def get_proposal_form(kind_slug):
    form_class = _get_tracker(kind_slug).form_class
    if not form_class:
        raise ValueError("No form class has been registered for proposal kind %r" % kind_slug)
    return form_class


def get_proposal_model_from_section_slug(section_slug):
    if section_slug not in trackers_by_section_slug:
        kind = ProposalKind.objects.get(section__slug=section_slug)
        trackers_by_section_slug[section_slug] = _get_tracker(kind.slug)
    model_class = trackers_by_section_slug[section_slug].model_class
    if not model_class:
        raise ValueError("No model class has been registered for section slug %r" % section_slug)
    return model_class


def get_kind_slugs():
    return trackers.keys()
