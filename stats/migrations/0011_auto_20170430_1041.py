# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_tradepoint_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradepoint',
            name='capacity',
            field=models.FloatField(default=0, verbose_name='Вместимость'),
        ),
        migrations.AddField(
            model_name='tradepoint',
            name='remaining_amount',
            field=models.FloatField(default=0, verbose_name='Оставшееся количество'),
        ),
    ]
