import os, hmac, subprocess
from django.http import HttpResponse, Http404
from django.utils import simplejson

import settings
from utils import log

def post_commit(request):
	log("Received connection from %s." % request.META['REMOTE_ADDR'])
	log("Headers: %s" % request.META)
	if request.method != 'POST':
		log("Returned an Http Response to GET request.")
		return HttpResponse("Google-hooks app for Google Code")
	payload = simplejson.loads(request.raw_post_data)
	project_name = payload['project_name']
	if project_name in settings.GOOGLEHOOKS_PROJECTS:
		project = settings.GOOGLEHOOKS_PROJECTS[project_name]
		given_key = request.META.get('HTTP_GOOGLE_CODE_PROJECT_HOSTING_HOOK_HMAC', None)
		if given_key is None:
			log("Raised 404 as host did not provide authentication key.")
			raise Http404
		m = hmac.new(project[0])
		m.update(request.raw_post_data)
		digest = m.hexdigest()
		if digest == given_key:
			try:
				project[1]()
			except TypeError:
				if isinstance(project[1], basestring):
					p = subprocess.Popen(project[1], shell=True, stdout=subprocess.PIPE)
					stdoutdata, stderrdata = p.communicate()
        			output = stdoutdata.strip()
        			error = stderrdata.strip()
        		else:
					log("ERROR: Not a callable object or string.")
					return Http404
			#except:
			#	log("ERROR: Callable object raised exception.")
			#	return Http404
		else:
			log("ERROR: Server did not successfully authenticate.")
			return Http404
	else:
		log("Raised 404, as project '%s' does not exist in GOOGLEHOOKS_PROJECTS." % project_name)
		raise Http404
	return HttpResponse()
