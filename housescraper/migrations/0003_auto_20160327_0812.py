# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-27 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housescraper', '0002_sourceinfo_hs_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='area',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='count',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='greenrate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='holdrate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='onrent',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='onsale',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='parklot',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='rentrate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='sourceinfo',
            name='cm_area',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sourceinfo',
            name='cm_count',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sourceinfo',
            name='cm_greenrate',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sourceinfo',
            name='cm_holdrate',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sourceinfo',
            name='cm_onrent',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sourceinfo',
            name='cm_onsale',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sourceinfo',
            name='cm_parklot',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sourceinfo',
            name='cm_rentrate',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
