# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order_position_close',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seg', models.CharField(default='NFO', max_length=128)),
                ('acc_id', models.CharField(max_length=128, null=True)),
                ('trade_name', models.CharField(max_length=255, null=True)),
                ('trade_qty', models.IntegerField(default=0)),
                ('trade_price', models.FloatField(default=0, max_length=10)),
                ('buy_or_sell', models.CharField(default='SELL', max_length=10)),
                ('trade_time', models.CharField(max_length=10)),
                ('b_w_l', models.CharField(max_length=10, null=True, blank=True)),
                ('user_id', models.CharField(max_length=128, null=True)),
                ('strike_price', models.FloatField(default=0, max_length=10)),
                ('expiry_date', models.DateField(null=True)),
                ('opt_type', models.CharField(max_length=2, null=True, choices=[('CE', 'Call'), ('PE', 'Put')])),
                ('symbol', models.CharField(max_length=255, null=True)),
                ('trade_date', models.DateField(default=datetime.date.today)),
                ('trade_uid', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order_position_open',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seg', models.CharField(default='NFO', max_length=128)),
                ('acc_id', models.CharField(max_length=128, null=True)),
                ('trade_name', models.CharField(max_length=255, null=True)),
                ('trade_qty', models.IntegerField(default=0)),
                ('trade_price', models.FloatField(default=0, max_length=10)),
                ('buy_or_sell', models.CharField(default='SELL', max_length=10)),
                ('trade_time', models.CharField(max_length=10)),
                ('b_w_l', models.CharField(max_length=10, null=True, blank=True)),
                ('user_id', models.CharField(max_length=128, null=True)),
                ('strike_price', models.FloatField(default=0, max_length=10)),
                ('expiry_date', models.DateField(null=True)),
                ('opt_type', models.CharField(max_length=2, null=True, choices=[('CE', 'Call'), ('PE', 'Put')])),
                ('symbol', models.CharField(max_length=255, null=True)),
                ('trade_date', models.DateField(default=datetime.date.today)),
                ('trade_uid', models.IntegerField(default=0)),
            ],
        ),
    ]
