# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_maker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_position_open',
            name='covering_rate',
            field=models.FloatField(default=0, max_length=10),
        ),
    ]
