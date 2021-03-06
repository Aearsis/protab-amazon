# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 01:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20170630_0136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'permissions': (('goods.can_mine', 'Insert tokens'), ('goods.can_sell', 'Sell goods')), 'verbose_name_plural': 'Goods'},
        ),
        migrations.AlterField(
            model_name='goodstype',
            name='type_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
