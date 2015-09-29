"""
Manage proposal kinds.

Everything is keyed off the ProposalKind slug value.
"""
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from symposion.conference.models import current_conference, Section, Conference
from symposion.proposals.models import ProposalKind, ProposalSection
from symposion.reviews.models import Review


class KindTracker(object):
    # Internal data structure
    def __init__(self, kind_slug):
        self.slug = kind_slug
        self.model_class = None
        self.form_class = None
        self.section_name = None


trackers = {}
trackers_by_section_slug = {}


def _get_tracker(slug):
    if slug not in trackers:
        trackers[slug] = KindTracker(slug)
    return trackers[slug]


def register_proposal_model(kind_slug, model_class, section_name):
    tracker = _get_tracker(kind_slug)
    tracker.model_class = model_class
    tracker.section_name = section_name


def register_proposal_form(kind_slug, form_class):
    _get_tracker(kind_slug).form_class = form_class


def get_proposal_model(kind_slug):
    model_class = _get_tracker(kind_slug).model_class
    if not model_class:
        raise ValueError("No model_class has been registered for proposal kind %r" % kind_slug)
    return model_class


def get_section_name(kind_slug):
    name = _get_tracker(kind_slug).section_name
    if not name:
        raise ValueError("No section_name has been registered for proposal kind %r" % kind_slug)
    return name


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


def ensure_proposal_records():
    """
    This can be called (after Django is done initializing) to make sure
    all the expected records exist for the defined kinds, including
    Permissions, ProposalKinds, ProposalSections, and Sections.

    It's invoked from symposion.proposals.signals on a post_migrate
    signal, so it gets run on each deploy automatically.

    It can also be invoked manually with the management command
    "ensure_proposal_records".
    """
    Conference.objects.get_or_create(pk=settings.CONFERENCE_ID)
    conference = current_conference()
    review_ct = ContentType.objects.get_for_model(Review)

    for kind_slug in get_kind_slugs():
        section_slug = kind_slug + "s"
        section_name = get_section_name(kind_slug)
        section, created = Section.objects.get_or_create(
            conference=conference,
            slug=section_slug,
            defaults=dict(
                name=section_name
            )
        )
        kind, created = ProposalKind.objects.get_or_create(
            slug=kind_slug,
            section=section,
            defaults=dict(
                name=section_name
            )
        )
        ProposalSection.objects.get_or_create(
            section=section,
            defaults=dict(
                closed=True,
                published=False,
            )
        )

        for verb in ['review', 'manage']:
            Permission.objects.get_or_create(
                codename='can_%s_%s' % (verb, section_slug),
                content_type=review_ct,
                defaults=dict(
                    name='Can %s %ss' % (verb, section.name),
                )
            )
