# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def no_op(apps, schema_editor):
    pass

def set_cached_tags(apps, schema_editor):
    ProposalBase = apps.get_model('proposals', 'ProposalBase')
    TaggedItem = apps.get_model('taggit', 'TaggedItem')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    try:
        content_type = ContentType.objects.get(
            app_label='proposals',
            model__iexact='ProposalBase'
        )
    except ContentType.DoesNotExist:
        # Initial migration, no content types yet, but no data needs migration either
        pass
    else:
        for proposal in ProposalBase.objects.all():
            items = TaggedItem.objects.filter(
                object_id=proposal.id,
                content_type_id=content_type.id,
            )
            names = items.values_list('tag__name', flat=True)
            proposal.cached_tags = ', '.join(names)
            proposal.save()


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_proposalbase_cached_tags'),
        ('taggit', '0001_initial'),
        ('contenttypes', '0001_initial')
    ]

    operations = [
        migrations.RunPython(set_cached_tags, no_op),
    ]
