# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-30 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartsearch', '0008_speciality_imagepath'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ponctualite',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='traitement',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
