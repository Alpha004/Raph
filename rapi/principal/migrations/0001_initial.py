# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 22:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NroCama', models.CharField(max_length=3)),
                ('Date', models.DateField()),
                ('Time', models.DateTimeField()),
                ('Description', models.TextField()),
                ('State', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('Lastname', models.CharField(max_length=30)),
                ('Username', models.CharField(max_length=30)),
                ('Password', models.CharField(max_length=30)),
                ('Email', models.CharField(max_length=30)),
                ('Track', models.CharField(max_length=6)),
            ],
        ),
    ]