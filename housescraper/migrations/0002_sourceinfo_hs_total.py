# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-21 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housescraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourceinfo',
            name='hs_total',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]