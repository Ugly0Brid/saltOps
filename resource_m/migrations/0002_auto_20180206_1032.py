# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-06 02:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource_m', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frame',
            name='cabinet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='frame_cabinet', to='resource_m.Cabinet', verbose_name='关联机柜'),
        ),
    ]
