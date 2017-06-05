# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-04 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0003_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend1', to='restapi.Users')),
                ('friend2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend2', to='restapi.Users')),
            ],
        ),
    ]