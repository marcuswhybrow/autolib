from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
# Model imports
from django.contrib.auth.models import User
from models import Book, Library, BookForm
# SOAP imports
from soaplib_handler import DjangoSoapApp, soapmethod, soap_types
from soaplib.client import make_service_client

def index(request):
	return render_to_response('books/book_list.html', {
		'books' : Book.objects.all(),
	})

# Book related views
def book(request, isbn):
	return render_to_response('books/book_detail.html', {
		'book' : get_object_or_404(Book, isbn=isbn),
	})

def book_add(request):
	if request.user.is_authenticated():
		args = {'form' : BookForm(), 'user' : request.user}
	else:
		args = {'error_message' : 'Please log in to add a book'}
	
	return render_to_response('books/book_add.html', args)


def book_add_handler(request):
	try:
		Book(isbn=request.POST['isbn'], title=request.POST['title'], author=request.POST['author'], library=Library(request.POST['library'])).save()
	except (KeyError):
		return render_to_response('books/book_add.html', {'error_message' : "That Book allready exists in your Library"})
	else:
		return HttpResponseRedirect(reverse('autolib.books.views.book', args=(request.POST['isbn'],)))
	
	
def profile(request):
	return render_to_response('books/profile.html', {
		'user' : request.user,
		'libraries' : Library.objects.filter(owner=request.user)
	})

# Library related views
def library_list(request):
	return render_to_response('books/library_list.html', {
		'libraries' : Library.objects.all(),
		'books' : Book.objects.all(),
		'users' : User.objects.all(),
	})


# SOAP view
class HelloWorldService(DjangoSoapApp):

	__tns__ = 'http://192.168.1.145:8000/'

	@soapmethod(soap_types.String, soap_types.Integer, _returns=soap_types.Array(soap_types.String))
	def say_hello(self, name, times):
		results = []
		for i in range(0, times):
			results.append('Hello, %s'%name)
		return results

hello_world_service = HelloWorldService()

def wsdl_doc(request):
	client = make_service_client('http://192.168.1.145:8000/hello_world/', HelloWorldService())
	wsdl = client.server.wsdl('')
	return HttpResponse(wsdl, mimetype='text/xml')