# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_auto_20170630_1106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='mined_time',
            new_name='mined_at',
        ),
    ]