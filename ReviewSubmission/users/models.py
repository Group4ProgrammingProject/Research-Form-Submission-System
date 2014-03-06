from django.db import models
from django.contrib.auth.models import User
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
    
#Submission models to be copied into a new app. Couldnt run Django properly on a different pc so i'll swap it over later


class Submission(models.Model):

    AWAITING_COMPLETION_CHECK = 0
    INCOMPLETE = 1
    AWAITING_APPROVAL = 2
    REJECTED = 3
    APPROVED = 4

    STATUS_CHOICE = (
        (AWAITING_COMPLETION_CHECK, 'Being checked for completion'),
        (INCOMPLETE, 'Incomplete'),
        (AWAITING_APPROVAL, 'Awaiting Approval'),
        (REJECTED, 'Rejected'),
        (APPROVED. 'Approved'),
    )

    user = models.OneToOneField(User, unique=True)
    status = models.IntegerField(default=AWAITING_COMPLETION_CHECK, choices=STATUS_CHOICE)
    

class SubmissionVersion(models.Model):
    application_form = models.FileField(upload_to=os.path.join(PROJECT_DIR,''))
    applicant_info = models.FileField(os.path.join(PROJECT_DIR, ''))
    consent_form = models.FileField(os.path.join(PROJECT_DIR, ''))
    submission = models.ForeignKey(Submission)


#Chat models ssame as above. I'll swap it over in a while

class Thread(models.Model):
    submission = models.ForeignKey(Submission)

class Message(models.Model):
    thread = models.ForeignKey(Thread)
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    written_at = models.DateTimeField(auto_add_now=True)

