# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finaid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('item', models.CharField(max_length=255)),
                ('amount', models.DecimalField(default=Decimal('0.00'), help_text='Please enter the amount of the receipt in US dollars.', verbose_name='Amount', max_digits=8, decimal_places=2)),
                ('new_file', models.ImageField(upload_to=b'finaid_receipts/')),
                ('application', models.ForeignKey(related_name='receipts', to='finaid.FinancialAidApplication')),
                ('user', models.ForeignKey(related_name='financial_aid_receipts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
