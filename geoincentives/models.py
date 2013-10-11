from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, null=True, blank=False)
    password = models.CharField(max_length=100, null=True, blank=False)
    email = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    first_name = models.CharField(max_length=128, null=True, blank=False)
    last_name = models.CharField(max_length=128, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    city = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    state = models.CharField(max_length=30, null=True, db_index=True, blank=False)
    zipcode = models.CharField(max_length=5, null=True, db_index=True, blank=False)
    school = models.CharField(max_length=255, null=True, db_index=True, blank=False)
    birthdate = models.DateField(blank=True, null=True)

class EventType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    max_checkin = models.IntegerField()

class Event(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    type = models.ForeignKey(EventType, null=True, blank=True)
    start_time = models.CharField(max_length=5, null=True, blank=False)
    end_time = models.CharField(max_length=5, null=True, blank=False)
    day = models.DateField()
    point_value = models.IntegerField()
    recurring = models.Booleanfield()



