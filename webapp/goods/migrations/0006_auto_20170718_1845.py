# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20170718_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodstype',
            name='type_id',
        ),
        migrations.AddField(
            model_name='goodstype',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
