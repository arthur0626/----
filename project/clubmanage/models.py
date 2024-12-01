# main/models.py
from django.db import models

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    song1 = models.CharField(max_length=45)
    song2 = models.CharField(max_length=45, blank=True, null=True)
    vocal = models.CharField(max_length=45, blank=True, null=True)
    guitar = models.CharField(max_length=45, blank=True, null=True)
    second_guitar = models.CharField(max_length=45, blank=True, null=True)
    bass = models.CharField(max_length=45, blank=True, null=True)
    drum = models.CharField(max_length=45, blank=True, null=True)
    keyboard = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    major = models.CharField(max_length=45)
    student_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=45)
    contact = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'user'


class UserAvailabledate(models.Model):
    user_id = models.IntegerField(primary_key=True)
    mon = models.IntegerField(blank=True, null=True)
    tue = models.IntegerField(blank=True, null=True)
    wed = models.IntegerField(blank=True, null=True)
    thu = models.IntegerField(blank=True, null=True)
    fri = models.IntegerField(blank=True, null=True)
    sat = models.IntegerField(blank=True, null=True)
    sun = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_availabledate'


class UserPrefergenre(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    k_pop = models.IntegerField(blank=True, null=True)
    j_pop = models.IntegerField(blank=True, null=True)
    pop = models.IntegerField(blank=True, null=True)
    hard = models.IntegerField(blank=True, null=True)
    indie = models.IntegerField(blank=True, null=True)
    ballad = models.IntegerField(blank=True, null=True)
    funk = models.IntegerField(blank=True, null=True)
    r_b = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_prefergenre'


class UserSessions(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    vocal = models.CharField(max_length=7, blank=True, null=True)
    guitar = models.CharField(max_length=7, blank=True, null=True)
    bass = models.CharField(max_length=7, blank=True, null=True)
    drum = models.CharField(max_length=7, blank=True, null=True)
    keyboard = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_sessions'