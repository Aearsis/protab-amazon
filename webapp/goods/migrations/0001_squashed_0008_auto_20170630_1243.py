# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 09:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('goods', '0001_initial'), ('goods', '0002_auto_20170630_0117'), ('goods', '0003_auto_20170630_0135'), ('goods', '0004_auto_20170630_0136'), ('goods', '0005_auto_20170630_0346'), ('goods', '0006_auto_20170630_1106'), ('goods', '0007_auto_20170630_1230'), ('goods', '0008_auto_20170630_1243')]

    initial = True

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('token', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name=6)),
                ('mined_time', models.DateField(default=None, null=True)),
                ('sold_at', models.DateField(default=None, null=True)),
                ('sold_for', models.IntegerField(default=None, null=True)),
                ('owner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='team.Team')),
            ],
            options={
                'permissions': (('insert_token', 'Insert tokens'), ('sell', 'Sell goods')),
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType'),
        ),
        migrations.AlterModelOptions(
            name='goods',
            options={'permissions': (('goods.can_mine', 'Insert tokens'), ('goods.can_sell', 'Sell goods')), 'verbose_name_plural': 'Goods'},
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='mined_time',
            new_name='mined_at',
        ),
        migrations.AlterField(
            model_name='goods',
            name='token',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
    ]