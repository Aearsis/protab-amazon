# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 09:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('chat', '0001_initial'), ('chat', '0002_auto_20170630_0151'), ('chat', '0003_auto_20170716_2134'), ('chat', '0004_auto_20170717_0957'), ('chat', '0005_auto_20170718_1026')]

    initial = True

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('players', models.ManyToManyField(to='team.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='team.Player')),
                ('channel', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='chat.Channel')),
                ('posted', models.DateTimeField(default=None)),
                ('visible', models.DateTimeField(default=None)),
            ],
            options={
                'ordering': ['posted'],
            },
        ),
    ]
