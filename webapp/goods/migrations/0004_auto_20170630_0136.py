# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 23:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20170630_0135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'permissions': (('goods.mine', 'Insert tokens'), ('goods.sell', 'Sell goods')), 'verbose_name_plural': 'Goods'},
        ),
    ]
