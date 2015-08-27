# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import now


def forward(apps, schema_editor):
    FinancialAidReviewData = apps.get_model('finaid', 'FinancialAidReviewData')

    # Where when_grant_letter_sent is not-null, we want grant_letter_sent to be True
    FinancialAidReviewData.objects.exclude(when_grant_letter_sent=None).update(grant_letter_sent=True)
    FinancialAidReviewData.objects.filter(when_grant_letter_sent=None).update(grant_letter_sent=False)


def backward(apps, schema_editor):
    FinancialAidReviewData = apps.get_model('finaid', 'FinancialAidReviewData')

    # Where grant_letter_sent is True and when_grant_letter_sent is None,
    # set when_grant_letter_sent to current timestamp for lack of an alternative
    FinancialAidReviewData.objects.filter(grant_letter_sent=True, when_grant_letter_sent=None).update(when_grant_letter_sent=now())


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0004_financialaidreviewdata_grant_letter_sent'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]
