from django.core.mail import EmailMessage
import json, datetime, random, string, urllib
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.conf import settings
from django import template
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.contrib.admin.views.decorators import staff_member_required

from models import Student, VerificationKey

def create_user(request):

	context = RequestContext(request)

	if all((x in request.POST for x in ['email', 'password'])):

		if User.objects.filter(email=request.POST['email']).count() > 0:
			print 'User Already Exists'
			template = get_template('login.html')
			return HttpResponse(template.render(context))

		else:
			#Username isn't important for this system so we'll just use the email. Less stuff for the user to fill out
			user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
			user.is_active = False
			user.save()

			#user = auth_authenticate(username=request.POST['email'], password=request.POST['password'])

			student = Student(user=user)
			student.save()

			#auth_login(request, user)
			verification_key = VerificationKey(key=(str(random.randint(111111111, 999999999)) + str(user.id)), user=user)
			verification_key.save()

			template = get_template('verification.html')

			url_data = { 'email' : user.username,'key' : verification_key.key }

			body = "Hi there!\n\tTo complete your registration please continue to the link below.\n\n" + (settings.SITE_NAME) + "verify/" + urllib.quote(user.username) + "/" + verification_key.key
			email = EmailMessage('Subject', body, 'ethicsboard5@gmail.com', [user.username])
			email.send()

			return HttpResponse(template.render(context))

	else:
		print "Please register first"
		return HttpResponseRedirect(reverse('dashboard'))

def dashboard(request):

	context = RequestContext(request)

	if not request.user.is_authenticated():
		template = get_template('login.html')
		return HttpResponse(template.render(context))

	if request.user.is_staff:
		template = get_template('staff_dashboard.html')
		return HttpResponse(template.render(context))

	else:
		template = get_template('dashboard.html')
		return HttpResponse(template.render(context))

	


def login(request):

	context = RequestContext(request)

	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('dashboard'))

	elif all((x in request.POST for x in ['email', 'password'])):
		email = request.POST['email']
		password = request.POST['password']
		user = auth_authenticate(username=email, password=password)
		auth_login(request, user)

		if user.is_active:
			template = get_template('dashboard.html')
		else:
			template = get_template('awaiting_verification.html')
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		template = get_template('dashboard.html')
		return HttpResponse(template.render(context))


def verify(request, email, key):

	context = RequestContext(request)
	user = User.objects.get(username=email)
	token = VerificationKey.objects.get(key=key, user=user)
	if token is not None and token.is_used is False:
		token.is_used = True
		user.is_active = True
		# user = auth_authenticate(username=email, password=user.password)
		# auth_login(request, user)
	user.save()
	token.save()

	template = get_template('login.html')
	return HttpResponse(template.render(context))

def accept_invite(request, key, email):

	context = RequestContext(request)
	user = Users.objects.get(username=email)
	token = InvitationKey.objects.get(key=key, user=user)
	if token is not None and token.is_used is False:
		token.is_used = False
		user.is_staff = True
	user.save()

	context['staff_email'] = email

	template = get_template('add_password.html')
	return HttpResponse(template.render(context))

@staff_member_required
def invite(request):

	context = RequestContext(request)
	if 'email' in request.POST:
		new_staff_member = User.objects.create_user(email=request.POST['email'])
		new_staff_member.is_active = False
		new_staff_member.save()

		invite_key = InviteKey(key=(str(random.randint(111111111, 999999999)) + str(user.id)), user=new_staff_member)
		invite_key.save()

		body = "Hi there!\n\tYou've been added as an administrator for the ethics board application review system. To complete your registration, please follow the link below\n\n" + (settings.SITE_NAME) + "accept_invite?key=" + invite_key.key + "&email=" + new_staff_member.username
		email = EmailMessage('Subject', body, 'ethicsboard5@gmail.com', [user.username])
		email.send()


def change_password(request):

	context = RequestContext(request)

	if all((x in request.POST for x in ['email', 'password'])):
		user = User.objects.get(username=request.POST['email'])
		user.password = request.POST['password']
		user.is_active = True
		user.save()

		auth_login(request, user)

	template = get_template('dashboard.html')
	return HttpResponse(template.render(context))


def logout(request):
	'''
	Logs a user out from the system and returns them to the homepage.
	'''

	context = RequestContext(request)
	auth.logout(request)
	template = get_template('login.html')
	return HttpResponse(template.render(context))
