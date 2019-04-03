# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finaid', '0014_auto_20190312_1503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receipt',
            options={'permissions': (('can_review_receipts', 'Review, Approve, and Flag Receipts'),)},
        ),
        migrations.AddField(
            model_name='receipt',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='receipt',
            name='approved_at',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='approved_by',
            field=models.ForeignKey(related_name='approved_finaid_receipts', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='receipt',
            name='flagged_at',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='flagged_by',
            field=models.ForeignKey(related_name='flagged_finaid_receipts', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='flagged_reason',
            field=models.CharField(default=None, max_length=1024, null=True, blank=True),
        ),
    ]
