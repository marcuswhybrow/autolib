from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

# Model imports
from django.contrib.auth.models import User
from libraries.models import Collection
from books.models import Book

# SOAP imports
from soaplib_handler import DjangoSoapApp, soapmethod, soap_types
from soaplib.client import make_service_client

from urllib import unquote_plus

from django.template import RequestContext
from django.views.generic.list_detail import object_list

### Views
### -----

def index(request):
	if request.user.is_authenticated():
		return render_to_response('libraries/index_authenticated.html', context_instance=RequestContext(request))
	return render_to_response('libraries/index_anonymous.html')

from libraries.models import CreateCollectionForm

@login_required
def library_list(request, template_name):
	queryset = request.user.libraries.all()
	return object_list(request, queryset=queryset, template_name=template_name, extra_context={'form': CreateCollectionForm(collection_type='library'),})

@login_required
def library_detail(request, library_name):
	return render_to_response('libraries/library_detail.html',{
		'library': get_object_or_404(Collection, name=unquote_plus(library_name), owner=request.user),
	}, context_instance=RequestContext(request))

@login_required
def bookshelf_detail(request, library_name, bookshelf_name):
	return render_to_response('libraries/bookshelf_detail.html',{
		'bookshelf': get_object_or_404(request.user.libraries.get(name=unquote_plus(library_name)).children, name=unquote_plus(bookshelf_name)),
	}, context_instance=RequestContext(request))

### SOAP
### ----

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