# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0012_auto_20160523_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edicion',
            name='TiempoE',
            field=models.DateTimeField(default=None),
        ),
    ]
