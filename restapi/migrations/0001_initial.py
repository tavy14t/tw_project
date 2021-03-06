# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-10 00:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('commentid', models.AutoField(db_column='commentId', primary_key=True, serialize=False)),
                ('userid', models.IntegerField(db_column='userId')),
                ('postid', models.IntegerField(db_column='postId')),
                ('text', models.TextField()),
            ],
            options={
                'db_table': 'COMMENTS',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('postid', models.AutoField(db_column='postId', primary_key=True, serialize=False)),
                ('userid', models.IntegerField(db_column='userId')),
                ('title', models.TextField()),
                ('body', models.TextField()),
            ],
            options={
                'db_table': 'POSTS',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PostsResources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postid', models.IntegerField(db_column='postId')),
                ('resourceid', models.IntegerField(db_column='resourceId')),
            ],
            options={
                'db_table': 'POSTS_RESOURCES',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PostsTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postid', models.IntegerField(db_column='postId')),
                ('tagid', models.IntegerField(db_column='tagId')),
            ],
            options={
                'db_table': 'POSTS_TAGS',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('resourceid', models.IntegerField(db_column='resourceId', primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('uri', models.TextField(db_column='URI')),
            ],
            options={
                'db_table': 'RESOURCES',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('tagid', models.IntegerField(db_column='tagId', primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'TAGS',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userid', models.IntegerField(db_column='userId', primary_key=True, serialize=False)),
                ('firstname', models.TextField(db_column='firstName')),
                ('lastname', models.TextField(db_column='lastName')),
                ('email', models.TextField()),
                ('passwordhash', models.TextField(db_column='passwordHash')),
                ('isactivated', models.TextField(blank=True, db_column='isActivated', null=True)),
                ('role', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'USERS',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(db_column='userId')),
                ('tagid', models.IntegerField(db_column='tagId')),
            ],
            options={
                'db_table': 'USERS_TAGS',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Avatars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.FileField(upload_to='avatars/%Y_%m_%d_%H_%M_%S')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.Users')),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend1', to='restapi.Users')),
                ('friend2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend2', to='restapi.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_userid', models.IntegerField()),
                ('to_roomid', models.IntegerField()),
                ('message', models.CharField(max_length=4000)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
