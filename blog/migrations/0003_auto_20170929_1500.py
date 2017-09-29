# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-29 14:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import picklefield.fields
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_specialist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', picklefield.fields.PickledObjectField(editable=False)),
                ('description', redactor.fields.RedactorField()),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, help_text='Optional photo post', null=True, upload_to='gallery/covers/%Y/%m/%d')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_avis', to='blog.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speciality_domain', to='blog.Domain')),
            ],
        ),
        migrations.RemoveField(
            model_name='specialist',
            name='domain',
        ),
        migrations.AddField(
            model_name='specialist',
            name='about_website',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='specialist',
            name='geocode',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='specialist',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speciality', to='blog.Speciality'),
        ),
        migrations.AddField(
            model_name='avis',
            name='specialist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialist_avis', to='blog.Specialist'),
        ),
    ]