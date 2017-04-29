# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 12:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_operator_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0), verbose_name='Продолжительность игры'),
        ),
        migrations.AlterField(
            model_name='game',
            name='start_time',
            field=models.DateTimeField(verbose_name='Время начала'),
        ),
    ]
