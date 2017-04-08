# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Answers(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    question = models.ForeignKey('Questions', models.DO_NOTHING)
    user_id = models.IntegerField()
    answer = models.TextField()
    solved = models.CharField(max_length=3)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    time_taken = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answers'


class Chapters(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=765)
    color = models.CharField(max_length=765, blank=True, null=True)
    description = models.TextField()
    display_order = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chapters'


class DeletedQuestions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    chapter = models.ForeignKey(Chapters, models.DO_NOTHING)
    user_id = models.IntegerField()
    deleted = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deleted_questions'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
# Unable to inspect table 'lista'
# The error was: ORA-22812: cannot reference nested table column's storage table



class Persoane(models.Model):
    nume = models.CharField(max_length=30, blank=True, null=True)
    prenume = models.TextField(unique=True, blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'persoane'


class QuestionCache(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField()
    quiz_question = models.ForeignKey('Questions', models.DO_NOTHING)
    quiz_chapter = models.ForeignKey(Chapters, models.DO_NOTHING)
    quiz_question_started_at = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question_cache'


class Questions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    chapter = models.ForeignKey(Chapters, models.DO_NOTHING)
    user_id = models.IntegerField(blank=True, null=True)
    question = models.TextField()
    answer = models.TextField()
    asked = models.IntegerField()
    solved = models.IntegerField()
    reported = models.IntegerField()
    report_resolved = models.IntegerField()
    created_at = models.DateTimeField(unique=True, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    report_solved = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questions'


class Reports(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    question = models.ForeignKey(Questions, models.DO_NOTHING)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports'


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    username = models.CharField(max_length=765)
    user_role = models.CharField(max_length=765)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Utilizatori(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nume = models.CharField(max_length=192)
    prenume = models.CharField(max_length=192)
    data_nastere = models.DateField()
    telefon = models.CharField(unique=True, max_length=96, blank=True, null=True)
    email = models.CharField(unique=True, max_length=384, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utilizatori'


class Zodiac(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=192)
    start_day = models.BigIntegerField()
    start_mon = models.BigIntegerField()
    end_day = models.BigIntegerField()
    end_mon = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'zodiac'
