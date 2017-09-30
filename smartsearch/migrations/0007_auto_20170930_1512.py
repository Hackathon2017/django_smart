# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-30 14:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartsearch', '0006_auto_20170930_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='specialist',
        ),
        migrations.AddField(
            model_name='rate',
            name='post',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='smartsearch.Post'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specialist',
            name='global_rate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]