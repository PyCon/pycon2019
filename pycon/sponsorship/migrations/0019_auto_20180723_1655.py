# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0018_sponsor_job_fair_participant'),
    ]

    operations = [
        migrations.CreateModel(
            name='BenefitPackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_words', models.PositiveIntegerField(null=True, verbose_name='max words', blank=True)),
                ('other_limits', models.CharField(max_length=200, verbose_name='other limits', blank=True)),
                ('benefit', models.ForeignKey(related_name='benefit_packages', verbose_name='benefit', to='sponsorship.Benefit')),
            ],
            options={
                'ordering': ['package'],
            },
        ),
        migrations.CreateModel(
            name='SponsorPackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('available', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('cost', models.PositiveIntegerField(verbose_name='cost')),
                ('description', models.TextField(help_text='This is private.', verbose_name='description', blank=True)),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference')),
            ],
            options={
                'ordering': ['conference', 'order'],
                'verbose_name': 'sponsor package',
                'verbose_name_plural': 'sponsor packages',
            },
        ),
        migrations.AddField(
            model_name='benefitpackage',
            name='package',
            field=models.ForeignKey(related_name='benefit_packages', verbose_name='package', to='sponsorship.SponsorPackage'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='packages',
            field=models.ManyToManyField(to='sponsorship.SponsorPackage', verbose_name='packages'),
        ),
    ]
