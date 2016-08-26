# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adhesin', '0006_auto_20160624_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedata',
            name='thr_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='filedata',
            name='pub_date',
            field=models.CharField(default=b'06_25_', max_length=12),
        ),
        migrations.AlterField(
            model_name='proteindata',
            name='pub_date',
            field=models.CharField(default=b'06_25_', max_length=10),
        ),
    ]
