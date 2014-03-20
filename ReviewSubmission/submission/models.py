from django.db import models
from django.contrib.auth.models import User
from time import time

import os
from django.conf import settings

def get_upload_file_name(isntance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.','_'),filename)

# Create your models here.
# class Submission(models.Model):
# 	pub_date = models.DateTimeField('date published')
# 	complete = models.BooleanField(default=False)
# 	application = models.FileField(upload_to=get_upload_file_name)


#class PersonalSubmission(models.Model):

#	pub_date = models.DateTimeField('date published')
#	complete = models.BooleanField()
#	application = models.FileField(upload_to=get_upload_file_name)

#class SubmissionVersion(models.Model):
#	pub_date = models.DateTimeField('date published')
#	most_recent = models.BooleanField(default=True) # needs to update to false if a newer version is submitted



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
		(APPROVED, 'Approved'),
	)

	user = models.OneToOneField(User, unique=True)
	status = models.IntegerField(default=AWAITING_COMPLETION_CHECK, choices=STATUS_CHOICE)


class Version(models.Model):
	application_form = models.FileField(upload_to=os.path.join(settings.PROJECT_DIR,''))
	applicant_info = models.FileField(upload_to=os.path.join(settings.PROJECT_DIR, ''))
	consent_form = models.FileField(upload_to=os.path.join(settings.PROJECT_DIR, ''))
	submission = models.ForeignKey(Submission)
