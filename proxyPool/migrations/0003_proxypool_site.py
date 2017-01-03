# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-03 05:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proxyPool', '0002_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxypool',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='proxyPool.Site', verbose_name='站点'),
        ),
    ]