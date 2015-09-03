# NB: This file should only be imported from the app's ready() function,
# to avoid signal handlers being hooked up multiple times.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from taggit.models import TaggedItem

from symposion.proposals.models import ProposalBase


# Use signals to update our cached tags whenever taggeditems
# that refer to proposals get updated.  Basically we want to
# figure out which proposal or proposals are affected and call
# .cache_tags() on them.
@receiver(post_save, sender=TaggedItem)
def tagitem_saved(sender, instance, raw, created, using, update_fields, **kwargs):
    """
    When a tagitem linked to a proposal changes, update the proposal
    it links to.
    """
    if not raw:
        thing_tagged = instance.content_object
        if isinstance(thing_tagged, ProposalBase):
            thing_tagged.cache_tags()


@receiver(post_delete, sender=TaggedItem)
def tagitem_deleted(sender, instance, **kwargs):
    """
    When a tagitem linked to a proposal is deleted, update the proposal
    it links to.
    """
    thing_tagged = instance.content_object
    if isinstance(thing_tagged, ProposalBase):
        ProposalBase.objects.get(id=instance.object_id).cache_tags()
