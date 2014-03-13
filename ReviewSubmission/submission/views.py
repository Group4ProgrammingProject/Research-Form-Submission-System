from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context
from submission.models import Submission
from forms import SubmissionForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
# Create your views here.

def submit_personal (request):
	name = "Personal Section:"
	t = get_template('submit_personal.html')
	html = t.render(Context({'name': name}))
	return render_to_response('submit_personal.html', context_instance=RequestContext(request))

def view_personal_submissions (request):
	name = "Personal Submissions View"
	t = get_template('personal_submission_view.html')
	html = t.render(Context({'name': name}))
	return render_to_response('personal_submission_view.html',context_instance=RequestContext(request))  
#return HttpResponse(html)

def submissions(request):
	return render_to_response('submissions.html',
	 {'submissions' :Submission.objects.All()})


# shows the first submission was saved correctly. was just for testing
def submission(request,article_id=1):
	return render_to_response('submission.html',
	 {'submission' :Submission.objects.get(id=article_id)})



def upload(request):
	if request.POST:
		form = SubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()

			return HttpResponseRedirect('/view_personal')
		else:
			form = SubmissionForm('/view_personal')

		args = {}
	args.update(csrf(request))

	args['form'] = form

	return render_to_response('personal_submission_view.html',args)







