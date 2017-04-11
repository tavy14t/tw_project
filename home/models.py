from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=160, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=510, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=256, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=300, blank=True, null=True)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    email = models.CharField(max_length=508, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Comments(models.Model):
    commentid = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    postid = models.ForeignKey('Posts', models.DO_NOTHING, db_column='postid')
    text = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'comments'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=400, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=510, blank=True, null=True)
    name = models.CharField(max_length=510, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=80)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Posts(models.Model):
    postid = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'posts'


class PostsTags(models.Model):
    postid = models.ForeignKey(Posts, models.DO_NOTHING, db_column='postid', blank=True, null=True)
    tagid = models.ForeignKey('Tags', models.DO_NOTHING, db_column='tagid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts_tags'


class Resources(models.Model):
    resourceid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    uri = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'resources'


class Tags(models.Model):
    tagid = models.BigIntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=128)
    timesuser = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class Users(models.Model):
    userid = models.BigIntegerField(primary_key=True)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.CharField(unique=True, max_length=128)
    passwordhash = models.CharField(max_length=32)
    isactivated = models.BooleanField()
    role = models.CharField(max_length=1)
    address = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersTags(models.Model):
    userid = models.ForeignKey(Users, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    tagid = models.ForeignKey(Tags, models.DO_NOTHING, db_column='tagid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_tags'
