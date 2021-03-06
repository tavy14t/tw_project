# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table # noqa
# Feel free to rename the models, but don't rename db_table values or
# field names.
from __future__ import unicode_literals

import json

from django.db import models
from channels import Group
from trex.settings import MSG_TYPE_MESSAGE


class Comments(models.Model):
    # Field name made lowercase.
    commentid = models.AutoField(db_column='commentId', primary_key=True)
    # Field name made lowercase.
    userid = models.IntegerField(db_column='userId')
    # Field name made lowercase.
    postid = models.IntegerField(db_column='postId')
    text = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'COMMENTS'


class Posts(models.Model):
    # Field name made lowercase.
    postid = models.AutoField(db_column='postId', primary_key=True)
    # Field name made lowercase.
    userid = models.IntegerField(db_column='userId')
    title = models.TextField()  # This field type is a guess.
    body = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'POSTS'


class PostsResources(models.Model):
    # Field name made lowercase.
    postid = models.IntegerField(db_column='postId')
    # Field name made lowercase.
    resourceid = models.IntegerField(db_column='resourceId')

    class Meta:
        managed = False
        db_table = 'POSTS_RESOURCES'


class Resources(models.Model):
    # Field name made lowercase.
    resourceid = models.IntegerField(db_column='resourceId', primary_key=True)
    name = models.TextField()  # This field type is a guess.
    # Field name made lowercase. This field type is a guess.
    uri = models.TextField(db_column='URI')

    class Meta:
        managed = False
        db_table = 'RESOURCES'


class Tags(models.Model):
    # Field name made lowercase.
    tagid = models.IntegerField(db_column='tagId', primary_key=True)
    name = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'TAGS'


class PostsTags(models.Model):
    # Field name made lowercase.
    postid = models.IntegerField(db_column='postId')
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE
    )
    # Field name made lowercase.
    tagid = models.IntegerField(db_column='tagId')
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE
    )

    class Meta:
        managed = False
        db_table = 'POSTS_TAGS'


class Users(models.Model):
    # Field name made lowercase.
    userid = models.IntegerField(db_column='userId', primary_key=True)
    # Field name made lowercase. This field type is a guess.
    firstname = models.TextField(db_column='firstName')
    # Field name made lowercase. This field type is a guess.
    lastname = models.TextField(db_column='lastName')
    email = models.TextField()  # This field type is a guess.
    # Field name made lowercase. This field type is a guess.
    passwordhash = models.TextField(db_column='passwordHash')
    # Field name made lowercase. This field type is a guess.
    isactivated = models.TextField(
        db_column='isActivated', blank=True, null=True)
    # This field type is a guess.
    role = models.TextField(blank=True, null=True)
    # This field type is a guess.
    address = models.TextField(blank=True, null=True)
    # This field type is a guess.
    phone = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'USERS'


class UsersTags(models.Model):
    # Field name made lowercase.
    userid = models.IntegerField(db_column='userId')
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )
    # Field name made lowercase.
    tagid = models.IntegerField(db_column='tagId')
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE
    )

    class Meta:
        managed = False
        db_table = 'USERS_TAGS'


class ChatRoom(models.Model):
    name = models.CharField(max_length=200)

    @property
    def websocket_group(self):
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        final_msg = {'room': str(self.id), 'message': message,
                     'username': user,
                     'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )


class Messages(models.Model):
    from_userid = models.IntegerField()
    to_roomid = models.IntegerField()
    message = models.CharField(max_length=4000)
    time = models.DateTimeField(auto_now_add=True)


class Friends(models.Model):
    friend1 = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='friend1',
    )

    friend2 = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='friend2',
    )


class Avatars(models.Model):
    url = models.FileField(upload_to='avatars')
    user = models.ForeignKey(Users)
