# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-10 23:55
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genotype',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('genotype_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/media/bhuvan/DATADRIVE1/gene-pc-api/data/23andme/raw'), upload_to='')),
                ('converted', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/media/bhuvan/DATADRIVE1/gene-pc-api/data/23andme/converted'), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('profile_id', models.CharField(max_length=100)),
                ('genotyped', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, editable=False, max_length=100)),
                ('profile_id', models.CharField(blank=True, editable=False, max_length=100)),
                ('token', models.CharField(blank=True, max_length=100, verbose_name='Bearer Token')),
                ('email', models.EmailField(blank=True, editable=False, max_length=254)),
                ('apiuserid', models.UUIDField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='twentythreeandme.User'),
        ),
        migrations.AddField(
            model_name='genotype',
            name='profile',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='twentythreeandme.Profile'),
        ),
    ]
