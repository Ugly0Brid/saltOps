# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-06 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource_m', '0002_auto_20180206_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='class_name',
            field=models.CharField(default='', max_length=50, verbose_name='类名'),
            preserve_default=False,
        ),
    ]