# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='newsType',
            field=models.CharField(choices=[('health', '健康'), ('tech', '科技'), ('eat', '饮食')], default=0, max_length=10),
            preserve_default=False,
        ),
    ]