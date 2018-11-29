# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorshipAvailability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipMentee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eligibility', models.IntegerField(default=1)),
                ('responded', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='mentorship_mentee', verbose_name=b'mentee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipMentor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('availability', models.IntegerField(default=1)),
                ('user', models.ForeignKey(related_name='mentorship_mentor', verbose_name=b'mentor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('finalized', models.BooleanField(default=False)),
                ('mentees', models.ManyToManyField(related_name='mentorship_mentee_sessions', to='mentorship.MentorshipMentee')),
                ('mentors', models.ManyToManyField(related_name='mentorship_mentor_sessions', to='mentorship.MentorshipMentor')),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='mentorshipsession',
            name='slot',
            field=models.ForeignKey(related_name='mentorship_session', verbose_name=b'mentorship slot', to='mentorship.MentorshipSlot'),
        ),
        migrations.AddField(
            model_name='mentorshipavailability',
            name='mentor',
            field=models.ForeignKey(related_name='mentorship_availability', verbose_name=b'mentorship availability', to='mentorship.MentorshipMentor'),
        ),
        migrations.AddField(
            model_name='mentorshipavailability',
            name='slot',
            field=models.ForeignKey(related_name='mentorship_availability', verbose_name=b'mentorship slot', to='mentorship.MentorshipSlot'),
        ),
    ]
