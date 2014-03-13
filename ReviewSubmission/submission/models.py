from django.db import models
from time import time

def get_upload_file_name(isntance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.','_'),filename)

# Create your models here.	
class Submission(models.Model):
	pub_date = models.DateTimeField('date published')
	complete = models.BooleanField(default=False)
	application = models.FileField(upload_to=get_upload_file_name)


#class PersonalSubmission(models.Model):

#	pub_date = models.DateTimeField('date published')
#	complete = models.BooleanField()
#	application = models.FileField(upload_to=get_upload_file_name)

#class SubmissionVersion(models.Model):
#	pub_date = models.DateTimeField('date published')
#	most_recent = models.BooleanField(default=True) # needs to update to false if a newer version is submitted
