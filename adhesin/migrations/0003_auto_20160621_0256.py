# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adhesin', '0002_auto_20160621_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='address',
            field=models.CharField(max_length=21),
        ),
    ]
