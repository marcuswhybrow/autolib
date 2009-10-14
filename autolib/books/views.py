from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
# Model imports
from django.contrib.auth.models import User
from models import Book, Library, BookForm

def index(request):
	return render_to_response('autolib/book_list.html', {
		'books' : Book.objects.all(),
	})

# Book related views
def book(request, isbn):
	return render_to_response('autolib/book_detail.html', {
		'book' : get_object_or_404(Book, isbn=isbn),
	})

def book_add(request):
	if request.user.is_authenticated():
		args = {'form' : BookForm(), 'user' : request.user}
	else:
		args = {'error_message' : 'Please log in to add a book'}
	
	return render_to_response('autolib/book_add.html', args)


def book_add_handler(request):
	try:
		Book(isbn=request.POST['isbn'], title=request.POST['title'], author=request.POST['author'], library=Library(request.POST['library'])).save()
	except (KeyError):
		return render_to_response('autolib/book_add.html', {'error_message' : "That Book allready exists in your Library"})
	else:
		return HttpResponseRedirect(reverse('autolib.books.views.book', args=(request.POST['isbn'],)))
	

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			# Redirect here to success page
			profile(request)
		else:
			login(request)
			# Account has been disabled
	else:
		login(request)
		# Incorrect login details

def profile(request):
	return render_to_response('autolib/profile.html', {
		'user' : request.user,
		'libraries' : Library.objects.filter(owner=request.user)
	})

# Library related views
def library_list(request):
	return render_to_response('autolib/library_list.html', {
		'libraries' : Library.objects.all(),
		'books' : Book.objects.all(),
		'users' : User.objects.all(),
	})
