# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-15 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=200)),
                ('speciality', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
            ],
        ),
    ]
