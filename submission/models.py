from django.db import models
from django.contrib.auth.models import User
from time import time

import os
from django.conf import settings

def get_upload_file_name(isntance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.','_'),filename)

class Submission(models.Model):

	AWAITING_UPLOAD = 0
	AWAITING_COMPLETION_CHECK = 1
	INCOMPLETE = 2
	AWAITING_APPROVAL = 3
	REJECTED = 4
	APPROVED = 5

	STATUS_CHOICE = (
		(AWAITING_UPLOAD, 'Awaiting application'),
		(AWAITING_COMPLETION_CHECK, 'Being checked for completion'),
		(INCOMPLETE, 'Incomplete'),
		(AWAITING_APPROVAL, 'Awaiting Approval'),
		(REJECTED, 'Rejected'),
		(APPROVED, 'Approved'),
	)

	user = models.OneToOneField(User)
	status = models.IntegerField(default=AWAITING_COMPLETION_CHECK, choices=STATUS_CHOICE)


class Version(models.Model):
	application_form = models.FileField(upload_to='documents/%Y/%m/%d')
	applicant_info = models.FileField(upload_to='documents/%Y/%m/%d')
	consent_form = models.FileField(upload_to='documents/%Y/%m/%d')
	submission = models.ForeignKey(Submission)
	pub_date = models.DateTimeField(auto_now_add=True)
