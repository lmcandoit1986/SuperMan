# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-06-16 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0003_performancedata_runt'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancedata',
            name='model',
            field=models.CharField(default=0, max_length=60),
            preserve_default=False,
        ),
    ]
