# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-29 22:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_post_specialist'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='specialist',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='specialist_avis', to='blog.Specialist'),
            preserve_default=False,
        ),
    ]
