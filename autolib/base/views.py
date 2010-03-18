from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from volumes.models import Book
from libraries.models import Collection
from base.models import Config

from django.template import RequestContext

### !Views
### ------

def index(request):
	if request.user.is_authenticated():
		return render_to_response('base/index_authenticated.html', context_instance=RequestContext(request))
	return render_to_response('base/index_anonymous.html')