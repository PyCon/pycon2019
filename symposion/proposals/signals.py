# NB: This file should only be imported from the app's ready() function,
# to avoid signal handlers being hooked up multiple times.

from django.db.models.signals import post_save, post_delete, post_migrate

from taggit.models import TaggedItem
from symposion.proposals.kinds import ensure_proposal_records
from symposion.proposals.models import ProposalBase


# Use signals to update our cached tags whenever taggeditems
# that refer to proposals get updated.  Basically we want to
# figure out which proposal or proposals are affected and call
# .cache_tags() on them.
def tagitem_saved(sender, instance, raw, created, using, update_fields, **kwargs):
    """
    When a tagitem linked to a proposal changes, update the proposal
    it links to.
    """
    if not raw:
        thing_tagged = instance.content_object
        if isinstance(thing_tagged, ProposalBase):
            thing_tagged.cache_tags()


def tagitem_deleted(sender, instance, **kwargs):
    """
    When a tagitem linked to a proposal is deleted, update the proposal
    it links to.
    """
    thing_tagged = instance.content_object
    if isinstance(thing_tagged, ProposalBase):
        ProposalBase.objects.get(id=instance.object_id).cache_tags()


# After migrating this app, make sure that we have all the right
# records for our proposal kinds.
def proposals_post_migrate(sender, app_config, **kwargs):
    if app_config.name == 'symposion.proposals':
        ensure_proposal_records()


def connect_signals():
    post_save.connect(tagitem_saved, sender=TaggedItem)
    post_delete.connect(tagitem_deleted, sender=TaggedItem)
    post_migrate.connect(proposals_post_migrate)
