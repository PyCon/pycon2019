# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PyConLightningTalkProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proposals.ProposalBase')),
                ('audience_level', models.IntegerField(help_text='Level of audience expertise assumed in Python.', verbose_name='Python level', choices=[(1, 'Novice'), (3, 'Intermediate'), (2, 'Experienced')])),
                ('overall_status', models.IntegerField(default=1, help_text='The status of the proposal.', choices=[(1, b'Not Yet Reviewed'), (2, b'In Kittendome'), (3, b'In Thunderdome'), (4, b'Accepted'), (5, b'Damaged'), (6, b'Rejected')])),
                ('damaged_score', models.IntegerField(help_text="Numerical indicator of the amount of interest in a talk set to 'damaged' status.", null=True, blank=True)),
                ('rejection_status', models.IntegerField(blank=True, help_text='The reason the proposal was rejected.', null=True, choices=[(1, b'Suggest re-submission as poster.'), (2, b'Suggest lightning talk.'), (3, b'Re-submitted under appropriate category.'), (4, b'Duplicate'), (5, b'Administrative Action (Other)'), (6, b"No really: rejected. It's just plain bad.")])),
                ('recording_release', models.BooleanField(default=True, help_text="By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2016/speaking/recording/' target='_blank'>PyCon 2016 Recording Release</a> for details.")),
                ('additional_requirements', models.TextField(help_text="Please let us know if you have any specific needs (A/V requirements, multiple microphones, a table, etc).  Note for example that 'audio out' is not provided for your computer unless you tell us in advance.", verbose_name='Additional requirements', blank=True)),
            ],
            options={
                'verbose_name': 'PyCon lightning talk proposal',
            },
            bases=('proposals.proposalbase',),
        ),
        migrations.CreateModel(
            name='PyConOpenSpaceProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proposals.ProposalBase')),
                ('audience_level', models.IntegerField(help_text='Level of audience expertise assumed in Python.', verbose_name='Python level', choices=[(1, 'Novice'), (3, 'Intermediate'), (2, 'Experienced')])),
                ('overall_status', models.IntegerField(default=1, help_text='The status of the proposal.', choices=[(1, b'Not Yet Reviewed'), (2, b'In Kittendome'), (3, b'In Thunderdome'), (4, b'Accepted'), (5, b'Damaged'), (6, b'Rejected')])),
                ('damaged_score', models.IntegerField(help_text="Numerical indicator of the amount of interest in a talk set to 'damaged' status.", null=True, blank=True)),
                ('rejection_status', models.IntegerField(blank=True, help_text='The reason the proposal was rejected.', null=True, choices=[(1, b'Suggest re-submission as poster.'), (2, b'Suggest lightning talk.'), (3, b'Re-submitted under appropriate category.'), (4, b'Duplicate'), (5, b'Administrative Action (Other)'), (6, b"No really: rejected. It's just plain bad.")])),
                ('recording_release', models.BooleanField(default=True, help_text="By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2016/speaking/recording/' target='_blank'>PyCon 2016 Recording Release</a> for details.")),
                ('additional_requirements', models.TextField(help_text="Please let us know if you have any specific needs (A/V requirements, multiple microphones, a table, etc).  Note for example that 'audio out' is not provided for your computer unless you tell us in advance.", verbose_name='Additional requirements', blank=True)),
            ],
            options={
                'verbose_name': 'PyCon Open Space proposal',
            },
            bases=('proposals.proposalbase',),
        ),
        migrations.CreateModel(
            name='PyConPosterProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proposals.ProposalBase')),
                ('audience_level', models.IntegerField(help_text='Level of audience expertise assumed in Python.', verbose_name='Python level', choices=[(1, 'Novice'), (3, 'Intermediate'), (2, 'Experienced')])),
                ('overall_status', models.IntegerField(default=1, help_text='The status of the proposal.', choices=[(1, b'Not Yet Reviewed'), (2, b'In Kittendome'), (3, b'In Thunderdome'), (4, b'Accepted'), (5, b'Damaged'), (6, b'Rejected')])),
                ('damaged_score', models.IntegerField(help_text="Numerical indicator of the amount of interest in a talk set to 'damaged' status.", null=True, blank=True)),
                ('rejection_status', models.IntegerField(blank=True, help_text='The reason the proposal was rejected.', null=True, choices=[(1, b'Suggest re-submission as poster.'), (2, b'Suggest lightning talk.'), (3, b'Re-submitted under appropriate category.'), (4, b'Duplicate'), (5, b'Administrative Action (Other)'), (6, b"No really: rejected. It's just plain bad.")])),
                ('recording_release', models.BooleanField(default=True, help_text="By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2016/speaking/recording/' target='_blank'>PyCon 2016 Recording Release</a> for details.")),
                ('additional_requirements', models.TextField(help_text="Please let us know if you have any specific needs (A/V requirements, multiple microphones, a table, etc).  Note for example that 'audio out' is not provided for your computer unless you tell us in advance.", verbose_name='Additional requirements', blank=True)),
            ],
            options={
                'verbose_name': 'PyCon Poster proposal',
            },
            bases=('proposals.proposalbase',),
        ),
        migrations.CreateModel(
            name='PyConProposalCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'PyCon proposal category',
                'verbose_name_plural': 'PyCon proposal categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PyConSponsorTutorialProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proposals.ProposalBase')),
            ],
            options={
                'verbose_name': 'PyCon Sponsor Tutorial proposal',
            },
            bases=('proposals.proposalbase',),
        ),
        migrations.CreateModel(
            name='PyConTalkProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proposals.ProposalBase')),
                ('audience_level', models.IntegerField(help_text='Level of audience expertise assumed in Python.', verbose_name='Python level', choices=[(1, 'Novice'), (3, 'Intermediate'), (2, 'Experienced')])),
                ('overall_status', models.IntegerField(default=1, help_text='The status of the proposal.', choices=[(1, b'Not Yet Reviewed'), (2, b'In Kittendome'), (3, b'In Thunderdome'), (4, b'Accepted'), (5, b'Damaged'), (6, b'Rejected')])),
                ('damaged_score', models.IntegerField(help_text="Numerical indicator of the amount of interest in a talk set to 'damaged' status.", null=True, blank=True)),
                ('rejection_status', models.IntegerField(blank=True, help_text='The reason the proposal was rejected.', null=True, choices=[(1, b'Suggest re-submission as poster.'), (2, b'Suggest lightning talk.'), (3, b'Re-submitted under appropriate category.'), (4, b'Duplicate'), (5, b'Administrative Action (Other)'), (6, b"No really: rejected. It's just plain bad.")])),
                ('recording_release', models.BooleanField(default=True, help_text="By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2016/speaking/recording/' target='_blank'>PyCon 2016 Recording Release</a> for details.")),
                ('additional_requirements', models.TextField(help_text="Please let us know if you have any specific needs (A/V requirements, multiple microphones, a table, etc).  Note for example that 'audio out' is not provided for your computer unless you tell us in advance.", verbose_name='Additional requirements', blank=True)),
                ('duration', models.IntegerField(choices=[(0, 'No preference'), (1, 'I prefer a 30 minute slot'), (2, 'I prefer a 45 minute slot')])),
                ('outline', models.TextField(verbose_name='Outline')),
                ('audience', models.CharField(help_text='Who is the intended audience for your talk? (Be specific; "Python programmers" is not a good answer to this question.)', max_length=150)),
                ('perceived_value', models.TextField(help_text="What will attendees get out of your talk? When they leave the room, what will they know that they didn't know before?", max_length=400, verbose_name='Objectives')),
                ('category', models.ForeignKey(to='pycon.PyConProposalCategory')),
            ],
            options={
                'verbose_name': 'PyCon talk proposal',
            },
            bases=('proposals.proposalbase',),
        ),
        migrations.CreateModel(
            name='PyConTutorialProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='proposals.ProposalBase')),
                ('audience_level', models.IntegerField(help_text='Level of audience expertise assumed in Python.', verbose_name='Python level', choices=[(1, 'Novice'), (3, 'Intermediate'), (2, 'Experienced')])),
                ('overall_status', models.IntegerField(default=1, help_text='The status of the proposal.', choices=[(1, b'Not Yet Reviewed'), (2, b'In Kittendome'), (3, b'In Thunderdome'), (4, b'Accepted'), (5, b'Damaged'), (6, b'Rejected')])),
                ('damaged_score', models.IntegerField(help_text="Numerical indicator of the amount of interest in a talk set to 'damaged' status.", null=True, blank=True)),
                ('rejection_status', models.IntegerField(blank=True, help_text='The reason the proposal was rejected.', null=True, choices=[(1, b'Suggest re-submission as poster.'), (2, b'Suggest lightning talk.'), (3, b'Re-submitted under appropriate category.'), (4, b'Duplicate'), (5, b'Administrative Action (Other)'), (6, b"No really: rejected. It's just plain bad.")])),
                ('recording_release', models.BooleanField(default=True, help_text="By submitting your talk proposal, you agree to give permission to the Python Software Foundation to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box. See <a href='https://us.pycon.org/2016/speaking/recording/' target='_blank'>PyCon 2016 Recording Release</a> for details.")),
                ('additional_requirements', models.TextField(help_text="Please let us know if you have any specific needs (A/V requirements, multiple microphones, a table, etc).  Note for example that 'audio out' is not provided for your computer unless you tell us in advance.", verbose_name='Additional requirements', blank=True)),
                ('domain_level', models.IntegerField(help_text="Level of audience expertise assumed in the presentation's domain.", choices=[(1, 'Novice'), (3, 'Intermediate'), (2, 'Experienced')])),
                ('outline', models.TextField(verbose_name='Outline')),
                ('more_info', models.TextField(help_text='More info. Will be made public if your talk is accepted.', verbose_name='More info')),
                ('audience', models.CharField(help_text='Who is the intended audience for your talk? (Be specific; "Python programmers" is not a good answer to this question.)', max_length=150)),
                ('perceived_value', models.TextField(help_text="What will attendees get out of your talk? When they leave the room, what will they know that they didn't know before?", max_length=500, verbose_name='Objectives')),
                ('handout', models.FileField(help_text='Upload a resource to be distributed to students  attending the tutorial session.', upload_to=b'tutorial_handouts', null=True, verbose_name='Student Handout', blank=True)),
                ('registration_count', models.IntegerField(default=0, help_text="Count of attendees. Allows inclusion of folks who don't have a PyCon account.", editable=False)),
                ('max_attendees', models.IntegerField(help_text='Maximum number of attendees, per CTE data', null=True, editable=False, blank=True)),
                ('category', models.ForeignKey(to='pycon.PyConProposalCategory')),
                ('registrants', models.ManyToManyField(help_text='CTE registered participants for this tutorial.', to=settings.AUTH_USER_MODEL, null=True, editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'PyCon tutorial proposal',
            },
            bases=('proposals.proposalbase',),
        ),
        migrations.CreateModel(
            name='ThunderdomeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=250)),
                ('code', models.CharField(unique=True, max_length=20)),
                ('decided', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pycontalkproposal',
            name='thunderdome_group',
            field=models.ForeignKey(related_name='talks', default=None, blank=True, to='pycon.ThunderdomeGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pyconposterproposal',
            name='category',
            field=models.ForeignKey(to='pycon.PyConProposalCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pyconopenspaceproposal',
            name='category',
            field=models.ForeignKey(to='pycon.PyConProposalCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pyconlightningtalkproposal',
            name='category',
            field=models.ForeignKey(to='pycon.PyConProposalCategory'),
            preserve_default=True,
        ),
    ]
