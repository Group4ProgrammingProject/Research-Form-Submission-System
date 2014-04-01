from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
#from django.contrib.auth.models import AbstractUser
#from simple_email_confirmation import SimpleEmailConfirmationUserMixin

class Student(models.Model):
	user = models.OneToOneField(User, unique=True)

User.profile = property(lambda u: Student.objects.get_or_create(user=u)[0])

class VerificationKey(models.Model):
    key = models.CharField(unique=True, max_length=250)
    user = models.OneToOneField(User, unique=True)
    is_used = models.BooleanField(default=False)


class InviteKey(models.Model):
    key = models.CharField(unique=True, max_length=250)
    user = models.OneToOneField(User, unique=True)
    is_used = models.BooleanField(default=False)
