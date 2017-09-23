# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0005_auto_20161002_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='financial_support',
            field=models.BooleanField(default=False, help_text='PyCon does not want expenses to discourage you from submitting a proposal, and offers financial support with a preference for speakers. Check here to indicate that you require assistance. This is not seen by the proposal reviewers and does not affect the review of  your proposal.'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='interested_mentee',
            field=multiselectfield.db.fields.MultiSelectField(help_text="I'm interested in receiving mentorship from others for my proposals in the following ways:", max_length=47, choices=[(b'brainstorming', b'Brainstorming'), (b'proposal_creation', b'Proposal Creation'), (b'proposal_review', b'Proposal Review')]),
        ),
        migrations.AddField(
            model_name='speaker',
            name='interested_mentor',
            field=multiselectfield.db.fields.MultiSelectField(help_text="I'm interested in providing mentorship for others submitting proposals in the following ways:", max_length=47, choices=[(b'brainstorming', b'Brainstorming'), (b'proposal_creation', b'Proposal Creation'), (b'proposal_review', b'Proposal Review')]),
        ),
    ]
