# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-31 13:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
            ],
            options={
                'verbose_name': '机柜',
            },
        ),
        migrations.CreateModel(
            name='DataCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('data_center_type', models.IntegerField(choices=[(0, '线上机房'), (1, '容灾机房')], default=0, verbose_name='类型')),
                ('link_name', models.CharField(max_length=255, verbose_name='联系人')),
                ('band_width', models.CharField(max_length=255, verbose_name='带宽')),
                ('contact_phone', models.CharField(max_length=255, verbose_name='联系人电话')),
            ],
            options={
                'verbose_name': '机房',
            },
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('cabinet', models.ForeignKey(auto_created='frame_cabinet', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resource_m.Cabinet', verbose_name='关联机柜')),
            ],
            options={
                'verbose_name': '机架',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('label', models.CharField(max_length=255, verbose_name='标签')),
            ],
            options={
                'verbose_name': '组',
            },
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('label', models.CharField(max_length=255, verbose_name='标签')),
            ],
            options={
                'verbose_name': '领域',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('minion_name', models.CharField(max_length=255, verbose_name='Minion名称')),
                ('minion_status', models.IntegerField(choices=[(0, '关闭'), (1, '开启')], default=0, verbose_name='Minion状态')),
                ('os', models.CharField(max_length=255, verbose_name='OS')),
                ('cpu', models.CharField(max_length=255, verbose_name='CPU')),
                ('memory', models.CharField(max_length=255, verbose_name='内存')),
            ],
            options={
                'verbose_name': '服务器',
            },
        ),
        migrations.CreateModel(
            name='ServerIp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('ip', models.CharField(max_length=255, verbose_name='服务器IP')),
                ('mac', models.CharField(max_length=255, verbose_name='MAC地址')),
            ],
            options={
                'verbose_name': '服务器IP',
            },
        ),
        migrations.CreateModel(
            name='PmServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resource_m.Server')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '物理机',
            },
            bases=('resource_m.server',),
        ),
        migrations.CreateModel(
            name='VmServer',
            fields=[
                ('server_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resource_m.Server')),
                ('pm_server', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vm_pm', to='resource_m.PmServer', verbose_name='关联物理机')),
            ],
            options={
                'verbose_name': '虚拟机',
            },
            bases=('resource_m.server',),
        ),
        migrations.AddField(
            model_name='serverip',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ip_server', to='resource_m.Server', verbose_name='服务器'),
        ),
        migrations.AddField(
            model_name='server',
            name='frame',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='server_frame', to='resource_m.Frame', verbose_name='关联机架'),
        ),
        migrations.AddField(
            model_name='server',
            name='scope',
            field=models.ManyToManyField(blank=True, null=True, related_name='server_scope', to='resource_m.Scope', verbose_name='关联领域'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='data_center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cabinet_datacenter', to='resource_m.DataCenter', verbose_name='关联机房'),
        ),
    ]
