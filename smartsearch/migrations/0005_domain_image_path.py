# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-30 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsearch', '0004_auto_20170930_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='image_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
