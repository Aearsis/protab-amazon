# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 23:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'permissions': (('insert_token', 'Insert tokens'), ('sell', 'Sell goods')), 'verbose_name_plural': 'Goods'},
        ),
    ]
