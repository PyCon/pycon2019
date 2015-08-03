# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import pycon.finaid.models


class Migration(migrations.Migration):

    dependencies = [
        ('finaid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(help_text=b'Please enter a description of this receipt image.', max_length=255)),
                ('amount', models.DecimalField(default=Decimal('0.00'), help_text='Please enter the amount of the receipt in US dollars.', verbose_name='Amount', max_digits=8, decimal_places=2)),
                ('receipt_image', models.ImageField(upload_to=pycon.finaid.models.user_directory_path)),
                ('application', models.ForeignKey(related_name='receipts', to='finaid.FinancialAidApplication')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
