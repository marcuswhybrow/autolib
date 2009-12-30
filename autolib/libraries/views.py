# !Imports

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Model imports

from django.contrib.auth.models import User
from books.models import Book
from libraries.models import Collection
from base.models import Config
from libraries.forms import CreateCollectionForm

from libraries.utils import CurrentUser

# SOAP imports

from urllib import unquote_plus

# Templates

from django.template import RequestContext
from django.views.generic.list_detail import object_list

### !Views
### -----

@CurrentUser
@login_required
def library_list(request, username, template_name):
		queryset = request.user.libraries.all()
		return object_list(request, queryset=queryset, template_name=template_name, extra_context={
			'form': CreateCollectionForm(collection_type='library'),
			'breadcrumbs': [
				('Profile', reverse('users.views.user_detail', args=[request.user.username])),
				('Libraries', reverse('libraries.views.library_list', args=[request.user.username])),
			],
		})

@CurrentUser
@login_required
def library_detail(request, username, library_name):
	library = get_object_or_404(request.user.libraries, name=unquote_plus(library_name))
	return render_to_response('libraries/library_detail.html', {
		'library': library,
		'breadcrumbs': [
			('Profile', reverse('users.views.user_detail', args=[request.user.username])),
			('Libraries', reverse('libraries.views.library_list', args=[request.user.username])),
			(library.name, reverse('libraries.views.library_detail', args=[request.user.username, library.get_slug()])),
		],
	}, context_instance=RequestContext(request))

@CurrentUser
@login_required
def bookshelf_detail(request, username, library_name, bookshelf_name):
	# The parent library
	library = get_object_or_404(request.user.libraries, name=unquote_plus(library_name))
	
	# If the bookshelf is the unsorted bin, there is no representing collection,
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
	return render_to_response('libraries/bookshelf_detail.html', {
		'library': library,
		'bookshelf': bookshelf,
		'breadcrumbs': [
			('Profile', reverse('users.views.user_detail', args=[request.user.username])),
			('Libraries', reverse('libraries.views.library_list', args=[request.user.username])),
			(library.name, reverse('libraries.views.library_detail', args=[request.user.username, library.get_slug()])),
			(bookshelf_new_name, reverse('libraries.views.bookshelf_detail', args=[request.user.username, library.get_slug(), bookshelf_slug])),
		],
	}, context_instance=RequestContext(request))

@CurrentUser
@login_required
def book_detail(request, username, library_name, bookshelf_name, book_isbn, book_title):
	library = get_object_or_404(Collection, name=unquote_plus(library_name), owner=request.user)
	
	if bookshelf_name == Config.objects.get(key='unsorted_bin').slug:
		bookshelf = None
		bookshelf_new_name = Config.objects.get(key='unsorted_bin').value
		bookshelf_slug = Config.objects.get(key='unsorted_bin').slug
		book = get_object_or_404(library.books, isbn=book_isbn, collection=library)
	else:
		bookshelf = get_object_or_404(library.children, name=unquote_plus(bookshelf_name))
		bookshelf_new_name = bookshelf.name
		bookshelf_slug = bookshelf.get_slug()
		book = get_object_or_404(bookshelf.books, isbn=book_isbn, collection=bookshelf)
		
	real_book_title = book.get_slug()
	if real_book_title != book_title:
		return HttpResponseRedirect(reverse('libraries.views.book_detail', args=[username, library_name, bookshelf_slug, book_isbn, real_book_title]))
	else:
		return render_to_response('books/book_detail.html', {
			'library': library,
			'bookshelf': bookshelf,
			'book': book,
			'breadcrumbs': [
				('Profile', reverse('users.views.user_detail', args=[request.user.username])),
				('Libraries', reverse('libraries.views.library_list', args=[request.user.username])),
				(library.name, reverse('libraries.views.library_detail', args=[request.user.username, library.get_slug()])),
				(bookshelf_new_name, reverse('libraries.views.bookshelf_detail', args=[request.user.username, library.get_slug(), bookshelf_slug])),
				(book.title, reverse('libraries.views.book_detail', args=[request.user.username, library.get_slug(), bookshelf_slug, book_isbn, book_title])),
			],
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