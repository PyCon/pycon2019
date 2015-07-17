# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forward(apps, schema_editor):
    # Migrate sponsor emails from the Sponsor model to the new SponsorEmail model.
    Sponsor = apps.get_model('sponsorship', 'Sponsor')
    ContactEmail = apps.get_model('sponsorship', 'ContactEmail')
    db_alias = schema_editor.connection.alias
    for sponsor in Sponsor.objects.using(db_alias).exclude(contact_email=''):
        ContactEmail.objects.using(db_alias).get_or_create(
            sponsor=sponsor,
            email=sponsor.contact_email,
        )


def backward(apps, schema_editor):
    # Migrate sponsor emails from the SponsorEmail model to the Sponsor model.
    Sponsor = apps.get_model('sponsorship', 'Sponsor')
    ContactEmail = apps.get_model('sponsorship', 'ContactEmail')
    db_alias = schema_editor.connection.alias
    for sponsor in Sponsor.objects.using(db_alias):
        # We can only save one...
        contact_email = sponsor.contact_emails.first()
        if contact_email:
            sponsor.contact_email = contact_email.email
            sponsor.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0002_contactemail'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
