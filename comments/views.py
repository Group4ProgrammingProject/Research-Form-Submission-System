from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context
from comments.models import Message
from forms import CommentForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

def comments (request):
    	return render_to_response('comments.html', {'comments': Message.objects.all()})

def comment(request):
	if request.POST:
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()

			return HttpResponseRedirect('/comments/')
	else:
		form = CommentForm()

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render_to_response('comment.html', args)
