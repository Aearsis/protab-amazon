# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_playermenuitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='instr',
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
