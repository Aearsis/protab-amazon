# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20170718_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='sell_quest',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='sell_time_sec',
        ),
        migrations.AddField(
            model_name='goodstype',
            name='sell_quest',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goodstype',
            name='sell_time_sec',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
