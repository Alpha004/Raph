# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0006_auto_20160425_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atencion',
            name='DescripcionA',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='atencion',
            name='ID_P',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='principal.Personal'),
        ),
    ]
