from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class ProfileModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default=None,null=True)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=100,default=None)


class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now,blank=True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=10000)