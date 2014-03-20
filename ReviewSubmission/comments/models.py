from django.db import models
from submission.models import Submission
from django.contrib.auth.models import User
from django.conf import settings

class Thread(models.Model):
    submission = models.ForeignKey(Submission)

class Message(models.Model):
    thread = models.ForeignKey(Thread)
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    written_at = models.DateTimeField(auto_now_add=True)
