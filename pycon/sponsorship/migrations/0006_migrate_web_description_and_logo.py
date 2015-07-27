# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    Sponsor = apps.get_model('sponsorship', 'Sponsor')
    db_alias = schema_editor.connection.alias

    for sponsor in Sponsor.objects.using(db_alias):
        # Get web description and set on sponsor
        description = sponsor.sponsor_benefits.filter(benefit__name='Company Description').first()
        if description:
            sponsor.web_description = description.text
        logo = sponsor.sponsor_benefits.filter(benefit__name='Web logo').first()
        if logo:
            sponsor.web_logo = logo.upload
        sponsor.save()


def back(apps, schema_editor):
    Sponsor = apps.get_model('sponsorship', 'Sponsor')
    Benefit = apps.get_model('sponsorship', 'Benefit')
    SponsorBenefit = apps.get_model('sponsorship', 'SponsorBenefit')
    db_alias = schema_editor.connection.alias

    description_benefit = Benefit.objects.get(name='Company Description')
    logo_benefit = Benefit.objects.get(name='Web logo')

    for sponsor in Sponsor.objects.using(db_alias):
        benefit, __ = sponsor.sponsor_benefits.get_or_create(
            benefit=description_benefit,
            defaults=dict(
                active=True
            )
        )
        benefit.text = sponsor.web_description
        benefit.save()
        benefit, __ = sponsor.sponsor_benefits.get_or_create(
            benefit=logo_benefit,
            defaults=dict(
                active=True
            )
        )
        benefit.upload = sponsor.web_logo
        benefit.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0005_auto_20150721_1445'),
    ]

    operations = [
        migrations.RunPython(forward, back),
    ]
