# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0003_set_cached_tags'),
        ('pycon', '0004_specialevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='EduSummitTalkProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proposals.ProposalBase')),
                ('audience_level', models.IntegerField(help_text='Level of audience expertise assumed in Python.', verbose_name='Python level', choices=[(1, 'Novice'), (3, 'Intermediate'), (2, 'Experienced')])),
                ('overall_status', models.IntegerField(default=1, help_text='The status of the proposal.', choices=[(1, b'Not Yet Reviewed'), (2, b'In Kittendome'), (3, b'In Thunderdome'), (4, b'Accepted'), (5, b'Damaged'), (6, b'Rejected')])),
                ('damaged_score', models.IntegerField(help_text="Numerical indicator of the amount of interest in a talk set to 'damaged' status.", null=True, blank=True)),
                ('rejection_status', models.IntegerField(blank=True, help_text='The reason the proposal was rejected.', null=True, choices=[(1, b'Suggest re-submission as poster.'), (2, b'Suggest lightning talk.'), (3, b'Re-submitted under appropriate category.'), (4, b'Duplicate'), (5, b'Administrative Action (Other)'), (6, b"No really: rejected. It's just plain bad.")])),
                ('recording_release', models.BooleanField(default=True, help_text="By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2016/speaking/recording/' target='_blank'>PyCon 2016 Recording Release</a> for details.")),
                ('additional_requirements', models.TextField(help_text="Please let us know if you have any specific needs (A/V requirements, multiple microphones, a table, etc).  Note for example that 'audio out' is not provided for your computer unless you tell us in advance.", verbose_name='Additional requirements', blank=True)),
                ('category', models.ForeignKey(to='pycon.PyConProposalCategory')),
            ],
            options={
                'verbose_name': 'Python Education Summit talk proposal',
            },
            bases=('proposals.proposalbase',),
        ),
    ]
