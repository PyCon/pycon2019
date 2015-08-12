# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycon', '0003_auto_20150731_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('location', models.CharField(max_length=100)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('description', models.TextField(help_text=b'markdown')),
                ('published', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'PyCon Special Event',
            },
            bases=(models.Model,),
        ),
    ]
