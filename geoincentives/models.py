from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager

import hashlib

class User(models.Model):
    USER_TYPE = (
        (1, 'student'),
        (2, 'business')
    )

    auth_user = models.OneToOneField(DjangoUser)
    type = models.CharField(max_length=100, null=True, blank=False, choices=USER_TYPE, default=USER_TYPE[1])
    address = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    city = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    state = models.CharField(max_length=30, null=True, db_index=True, blank=False)
    zipcode = models.CharField(max_length=5, null=True, db_index=True, blank=False)
    school = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    birthdate = models.DateField(blank=True, null=True)

    @classmethod
    def hash_password(cls, password):
        return hashlib.sha224(password).hexdigest()

class EventType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    max_checkin = models.IntegerField()

class Event(models.Model):
    EVENT_STATUS = (
        (1, 'active'),
        (2, 'inactive')
    )

    name = models.CharField(max_length=255, null=True, blank=False)
    type = models.ForeignKey(EventType, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=False, choices=EVENT_STATUS)
    start_time = models.CharField(max_length=5, null=True, blank=False)
    end_time = models.CharField(max_length=5, null=True, blank=False)
    date = models.DateField()
    point_value = models.IntegerField()
    recurring = models.BooleanField()
    verified = models.BooleanField()
    address = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    city = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    state = models.CharField(max_length=30, null=True, db_index=True, blank=False)
    zipcode = models.CharField(max_length=5, null=True, db_index=True, blank=False)
    latitude = models.FloatField()
    longitude = models.FloatField()

class UserEvent(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    date = models.DateField()

class Reward(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    available = models.IntegerField()
    points = models.IntegerField()

