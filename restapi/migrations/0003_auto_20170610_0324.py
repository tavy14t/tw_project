# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-10 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_auto_20170610_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatars',
            name='url',
            field=models.FileField(upload_to='avatars'),
        ),
    ]
