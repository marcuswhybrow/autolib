from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from books.models import Book
from libraries.models import Collection
from base.models import Config
from libraries.forms import CreateCollectionForm
from libraries.utils import CurrentUser

from urllib import unquote_plus

from django.template import RequestContext
from django.views.generic.list_detail import object_list

### !Views
### -----

def user_list(request):
	return render_to_response('users/user_list.html', {
		'users': User.objects.all()
	}, context_instance=RequestContext(request))

def user_detail(request, username):
	return render_to_response('users/user_detail.html', {
		'user_detail': get_object_or_404(User, username=username),
    }, context_instance=RequestContext(request))

@CurrentUser
@login_required
def library_list(request, username, template_name):
		queryset = request.user.libraries.all()
		return object_list(request, queryset=queryset, template_name=template_name, extra_context={
			'user_detail': User.objects.get(username=username),
			'form': CreateCollectionForm(collection_type='library'),
		})

@CurrentUser
@login_required
def library_detail(request, username, library_name):
	library = get_object_or_404(request.user.libraries, name=unquote_plus(library_name))
	return render_to_response('users/library_detail.html', {
		'user_detail': User.objects.get(username=username),
		'library': library,
	}, context_instance=RequestContext(request))

@CurrentUser
@login_required
def bookshelf_detail(request, username, library_name, bookshelf_name):
	library = get_object_or_404(request.user.libraries, name=unquote_plus(library_name))
	
	# If the bookshelf is the unsorted bin, there is no collection object,
	# otherwise get the appropriate collection.
	if bookshelf_name == Config.objects.get(key='unsorted_bin').slug:
		bookshelf = None
		bookshelf_new_name = Config.objects.get(key='unsorted_bin').value
		bookshelf_slug = Config.objects.get(key='unsorted_bin').slug
	else:
		bookshelf = get_object_or_404(library.children, name=unquote_plus(bookshelf_name))
		bookshelf_new_name = bookshelf.name
		bookshelf_slug = bookshelf.get_slug()
	
	# Return the library and the bookshelf.
	return render_to_response('users/bookshelf_detail.html', {
		'user_detail': User.objects.get(username=username),
		'library': library,
		'bookshelf': bookshelf,
	}, context_instance=RequestContext(request))

@CurrentUser
@login_required
def book_detail(request, username, library_name, bookshelf_name, book_isbn, book_title=None):
	library = get_object_or_404(Collection, name=unquote_plus(library_name), owner=request.user)
	
	if bookshelf_name == Config.objects.get(key='unsorted_bin').slug:
		bookshelf = None
		bookshelf_new_name = Config.objects.get(key='unsorted_bin').value
		bookshelf_slug = Config.objects.get(key='unsorted_bin').slug
		book = get_object_or_404(library.books, book_instance=Book.objects.get(isbn=book_isbn), collection=library)
	else:
		bookshelf = get_object_or_404(library.children, name=unquote_plus(bookshelf_name))
		bookshelf_new_name = bookshelf.name
		bookshelf_slug = bookshelf.get_slug()
		book = get_object_or_404(bookshelf.books, book_instance=Book.objects.get(isbn=book_isbn), collection=bookshelf)
		
	real_book_title = book.get_slug()
	if real_book_title != book_title:
		return HttpResponseRedirect(reverse('users.views.book_detail', args=[
			username, 
			library_name, 
			bookshelf_slug, 
			book_isbn, 
			real_book_title
		]))
	else:
		return render_to_response('users/book_detail.html', {
			'user_detail': User.objects.get(username=username),
			'library': library,
			'bookshelf': bookshelf,
			'book': book,
		}, context_instance=RequestContext(request))

### !Form Views
### ----------

from django.db import IntegrityError
from.django import forms

@login_required
def create_collection(request, collection_type):
	
	if collection_type == 'library' or 'bookshelf' or 'series':
		if request.method == 'POST':
			# Collection.objects.get(name=parent, owner=request.user, type)
			form = CreateCollectionForm(request.POST, collection_type=collection_type, user=request.user)
			if form.is_valid():
				form.save()
		else:
			form = CreateCollectionForm(collection_type=collection_type)
				
		return render_to_response('libraries/'+collection_type+'_form.html', {
			'form': form,
			'parent': request.GET.get('parent', None),
		})
	raise AssertionError, 'When instantiating a create_collection form the collection_type argument must be one fo the following: "library", "bookshelf" or "series".'