# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adhesin', '0008_auto_20160702_0342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_details',
            name='id',
        ),
        migrations.AlterField(
            model_name='filedata',
            name='pub_date',
            field=models.CharField(default=b'07_05_', max_length=12),
        ),
        migrations.AlterField(
            model_name='proteindata',
            name='pub_date',
            field=models.CharField(default=b'07_05_', max_length=10),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='address',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
    ]
