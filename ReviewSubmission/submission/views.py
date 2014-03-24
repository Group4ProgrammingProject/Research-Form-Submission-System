from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context
from submission.models import Submission
from submission.forms import SubmissionForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

from django.core.urlresolvers import reverse

from submission.models import Submission, Version
from submission.forms import SubmissionForm

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





def list_files(request, subm_id):
    # Handle file upload

    context = RequestContext(request)

    user = request.user

    context["user"] = user

    try:
    	submission = Submission.objects.get(pk=user.id)
    except:
    	submission = Submission(user=user)
        submission.save()

    if request.method == 'POST':
        # form = SubmissionForm(request.POST, request.FILES)
        if all((x in request.FILES for x in ['app_form', 'app_info', 'con_form'])):

            newdoc = Version(
            	application_form=request.FILES['app_form'],
            	applicant_info=request.FILES['app_info'],
            	consent_form=request.FILES['con_form'],
            	submission=submission)
            newdoc.save()

            # Redirect to the document list after POST
            template = get_template('dashboard.html')  
            return HttpResponse(template.render(context))
    else:
        form = SubmissionForm() # A empty, unbound form
        context["form"] = form

    # Load documents for the list page
    versions = Version.objects.filter(submission=submission)

    context["versions"] = versions
    context["submission"] = submission

    template = get_template('file_list.html')
    return HttpResponse(template.render(context))

    # # Render list page with the documents and the form
    # return render_to_response(
    #     'myapp/list.html',
    #     {'documents': documents, 'form': form},
    #     context_instance=RequestContext(request)
    # )