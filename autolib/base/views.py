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

### !SOAP
### -----

from soaplib_handler import DjangoSoapApp, soapmethod, soap_types
from soaplib.client import make_service_client

class HelloWorldService(DjangoSoapApp):

	__tns__ = 'http://autolib.marcuswhybrow.net/api/'

	@soapmethod(soap_types.String, soap_types.Integer, _returns=soap_types.Array(soap_types.String))
	def say_hello(self, name, times):
		results = []
		for i in range(0, times):
			results.append('Hello, %s'%name)
		return results

hello_world_service = HelloWorldService()

def wsdl_doc(request):
	client = make_service_client('http://autolib.marcuswhybrow.net/api/', HelloWorldService())
	return HttpResponse(client.server.wsdl(''), mimetype='text/xml')