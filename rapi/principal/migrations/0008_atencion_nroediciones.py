# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-27 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_auto_20160425_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='atencion',
            name='NroEdiciones',
            field=models.IntegerField(default=0),
        ),
    ]
