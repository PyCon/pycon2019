# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


OBSOLETE_BENEFITS = [
    {'name': 'Company URL',
     'type': 'simple',
     },
    {'name': 'Company Description',
     'type': 'text',
     },
    {'name': 'Web logo',
     'type': 'weblogo',
     }
]


def forward(apps, schema_editor):
    Benefit = apps.get_model('sponsorship', 'Benefit')
    BenefitLevel = apps.get_model('sponsorship', 'BenefitLevel')
    SponsorBenefit = apps.get_model('sponsorship', 'SponsorBenefit')
    db_alias = schema_editor.connection.alias

    names = [b['name'] for b in OBSOLETE_BENEFITS]

    # Clean up other records that use these first
    BenefitLevel.objects.using(db_alias).filter(benefit__name__in=names).delete()
    SponsorBenefit.objects.using(db_alias).filter(benefit__name__in=names).delete()

    # Now we can remove the Benefit records themselves
    Benefit.objects.using(db_alias).filter(name__in=names).delete()


def back(apps, schema_editor):
    Benefit = apps.get_model('sponsorship', 'Benefit')
    db_alias = schema_editor.connection.alias

    for ben in OBSOLETE_BENEFITS:
        Benefit.objects.using(db_alias).get_or_create(**ben)


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0007_auto_20150721_1533'),
    ]

    operations = [
        migrations.RunPython(forward, back),
    ]
