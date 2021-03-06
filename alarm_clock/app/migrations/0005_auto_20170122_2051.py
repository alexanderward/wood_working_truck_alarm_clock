# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 02:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170119_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='last_edited_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video', to='app.Video'),
        ),
    ]
