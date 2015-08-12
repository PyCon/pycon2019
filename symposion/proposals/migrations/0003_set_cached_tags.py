# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def no_op(apps, schema_editor):
    pass

def set_cached_tags(apps, schema_editor):
    TaggedItem = apps.get_model('taggit', 'TaggedItem')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    to_migrate = [
        ('pycon', 'PyConTalkProposal'),
        ('pycon', 'PyConLightningTalkProposal'),
        ('pycon', 'PyConTutorialProposal'),
        ('pycon', 'PyConPosterProposal'),
        ('pycon', 'PyConSponsorTutorialProposal'),
        ('pycon', 'PyConOpenSpaceProposal'),
    ]

    for app_label, model_name in to_migrate:
        model = apps.get_model(app_label, model_name)
        try:
            ct = ContentType.objects.get(app_label=app_label, model__iexact=model_name)
        except ContentType.DoesNotExist:
            # If the content type for a proposal model doesn't exist, this
            # must be the initial migration, with no data. So, nothing to
            # cache tags for anyway.
            pass
        else:
            for proposal in model.objects.all():
                items = TaggedItem.objects.filter(
                    object_id=proposal.id,
                    content_type_id=ct.id,
                )
                names = items.values_list('tag__name', flat=True)
                proposal.cached_tags = ', '.join(names)
                proposal.save()


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_proposalbase_cached_tags'),
        ('taggit', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('pycon', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_cached_tags, no_op),
    ]
