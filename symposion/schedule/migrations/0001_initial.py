# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0001_initial'),
        ('proposals', '0001_initial'),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('abstract', models.TextField()),
                ('cancelled', models.BooleanField(default=False)),
                ('additional_speakers', models.ManyToManyField(related_name='copresentations', to='speakers.Speaker', blank=True)),
                ('proposal_base', models.OneToOneField(related_name='presentation', to='proposals.ProposalBase')),
                ('section', models.ForeignKey(related_name='presentations', to='conference.Section')),
            ],
            options={
                'ordering': ['slot'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=65)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=True)),
                ('section', models.OneToOneField(to='conference.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('content_override', models.TextField(blank=True)),
                ('day', models.ForeignKey(to='symposion_schedule.Day')),
            ],
            options={
                'ordering': ['day', 'start', 'end'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlotKind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('schedule', models.ForeignKey(to='symposion_schedule.Schedule')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlotRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room', models.ForeignKey(to='symposion_schedule.Room')),
                ('slot', models.ForeignKey(to='symposion_schedule.Slot')),
            ],
            options={
                'ordering': ['slot', 'room__order'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='slotroom',
            unique_together=set([('slot', 'room')]),
        ),
        migrations.AddField(
            model_name='slot',
            name='kind',
            field=models.ForeignKey(verbose_name=b'slot kind', to='symposion_schedule.SlotKind'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='schedule',
            field=models.ForeignKey(to='symposion_schedule.Schedule'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='presentation',
            name='slot',
            field=models.OneToOneField(related_name='content_ptr', null=True, blank=True, to='symposion_schedule.Slot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='presentation',
            name='speaker',
            field=models.ForeignKey(related_name='presentations', to='speakers.Speaker'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='day',
            name='schedule',
            field=models.ForeignKey(to='symposion_schedule.Schedule'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('schedule', 'date')]),
        ),
    ]
