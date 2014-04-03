from django import forms
from models import Submission, Version

class SubmissionForm(forms.ModelForm):

	class Meta:
		model = Version

	application_form = forms.FileField(label='Select a file')
	applicant_info = forms.FileField(label='Select a file')
	consent_form = forms.FileField(label='Select a file')