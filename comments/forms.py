from django import forms
from models import Message

class CommentForm(forms.ModelForm):

	class Meta:
		model = Message
		fields = ('user','message')
