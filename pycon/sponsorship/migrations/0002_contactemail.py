# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0001_initial'),
    ]

    operations = [
        # Make contact_email have a default, so in the reverse, it's okay to add the field
        # before we have put values into it.
        migrations.AlterField(
            model_name='sponsor',
            name='contact_email',
            field=models.EmailField(max_length=75, verbose_name='Contact Email', blank=True, default=''),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ContactEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, verbose_name='Contact Email')),
                ('sponsor', models.ForeignKey(related_name='contact_emails', to='sponsorship.Sponsor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='contactemail',
            unique_together=set([('sponsor', 'email')]),
        ),
    ]
