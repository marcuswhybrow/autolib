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

# SOAP imports

from urllib import unquote_plus

# Templates

from django.template import RequestContext
from django.views.generic.list_detail import object_list

### !Views
### -----

@login_required
def library_list(request, template_name):
	queryset = request.user.libraries.all()
	return object_list(request, queryset=queryset, template_name=template_name, extra_context={'form': CreateCollectionForm(collection_type='library'),})

@login_required
def library_detail(request, library_name):
	return render_to_response('libraries/library_detail.html', {
		'library': get_object_or_404(request.user.libraries, name=unquote_plus(library_name)),
	}, context_instance=RequestContext(request))

@login_required
def bookshelf_detail(request, library_name, bookshelf_name):
	# The parent library
	library = get_object_or_404(request.user.libraries, name=unquote_plus(library_name))
	
	# If the bookshelf is the unsorted bin, there is no representing collection,
	# otherwise get the appropriate collection.
	if bookshelf_name == Config.objects.get(key='unsorted_bin').slug:
		bookshelf = None
	else:
		bookshelf = get_object_or_404(library.children, name=unquote_plus(bookshelf_name))
	
	# Return the library and the bookshelf.
	return render_to_response('libraries/bookshelf_detail.html', {
		'library': library,
		'bookshelf': bookshelf,
	}, context_instance=RequestContext(request))

@login_required
def book_detail(request, library_name, bookshelf_name, book_isbn):
	library = get_object_or_404(Collection, name=unquote_plus(library_name), owner=request.user)
	bookshelf = get_object_or_404(library.children, name=unquote_plus(bookshelf_name)),
	book = get_object_or_404(bookshelf.children)
	
	return render_to_response('libraries/book_detail.html', {
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