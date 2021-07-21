from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import json


def get_default_profile_image():
    return "images/dummy_image.png"

class ProfileModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default=None,null=True)
    email = models.EmailField(null=True)
    profile_image = models.ImageField(max_length=500, upload_to="profile_images/", null=True, blank=True,
                                      default=get_default_profile_image)
    username = models.CharField(max_length=100)


class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now,blank=True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=10000)

class Group(models.Model):
    name = models.CharField(max_length=1000)
    users = models.CharField(max_length=2000)

class GroupMessages(models.Model):
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=100)
    group = models.CharField(max_length=10000)

class AddMembers(models.Model):
    member = models.CharField(max_length=100)
    group_id = models.CharField(max_length=100)