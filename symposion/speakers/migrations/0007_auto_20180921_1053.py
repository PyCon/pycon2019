# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0006_speaker_profile_flags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='interested_mentee',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=47, null=True, choices=[(b'brainstorming', b'Brainstorming'), (b'proposal_creation', b'Proposal Creation'), (b'proposal_review', b'Proposal Review')]),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='interested_mentor',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=47, null=True, choices=[(b'brainstorming', b'Brainstorming'), (b'proposal_creation', b'Proposal Creation'), (b'proposal_review', b'Proposal Review')]),
        ),
    ]
