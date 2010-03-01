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

from django.db.models import Q

@login_required
def add_books(request):
	collection_pk = request.GET.get('c', None)
	try:
		collection = Collection.objects.get(Q(pk=collection_pk)& (Q(owner=request.user) | Q(parent__owner=request.user) | Q(parent__parent__owner=request.user)))
	except Collection.DoesNotExist:
		collection = None
	
	return render_to_response('libraries/addbooks.html', {
		'collection': collection,
	}, context_instance=RequestContext(request))

@login_required
def library_list(request, template_name):
	queryset = request.user.libraries.all()
	return object_list(request, queryset=queryset, template_name=template_name, extra_context={
		'form': CreateCollectionForm(),
	})

@login_required
def library_detail(request, library_name):
	library = get_object_or_404(request.user.libraries, slug=library_name)
	return render_to_response('libraries/library_detail.html', {
		'library': library,
		'form': CreateCollectionForm(),
	}, context_instance=RequestContext(request))

@login_required
def bookshelf_detail(request, library_name, bookshelf_name):
	library = get_object_or_404(request.user.libraries, slug=library_name)
	
	# If the bookshelf is the unsorted bin, there is no collection object,
	# otherwise get the appropriate collection.
	if bookshelf_name == Config.objects.get(key='unsorted_bin').slug:
		bookshelf = None
		bookshelf_new_name = Config.objects.get(key='unsorted_bin').value
		bookshelf_slug = Config.objects.get(key='unsorted_bin').slug
	else:
		bookshelf = get_object_or_404(library.children, slug=bookshelf_name)
		bookshelf_new_name = bookshelf.name
		bookshelf_slug = bookshelf.slug
	
	# Return the library and the bookshelf.
	return render_to_response('libraries/bookshelf_detail.html', {
		'library': library,
		'bookshelf': bookshelf,
	}, context_instance=RequestContext(request))

@login_required
def profile_detail(request, library_name, bookshelf_name, book_isbn, book_title=None):
	library = get_object_or_404(Collection, slug=library_name, owner=request.user)
	
	if bookshelf_name == Config.objects.get(key='unsorted_bin').slug:
		bookshelf = None
		bookshelf_new_name = Config.objects.get(key='unsorted_bin').value
		bookshelf_slug = Config.objects.get(key='unsorted_bin').slug
		book = get_object_or_404(library.books, book_instance=Book.objects.get(isbn10=book_isbn), collection=library)
	else:
		bookshelf = get_object_or_404(library.children, slug=bookshelf_name)
		bookshelf_new_name = bookshelf.name
		bookshelf_slug = bookshelf.slug
		book = get_object_or_404(bookshelf.books, book_instance=Book.objects.get(isbn10=book_isbn), collection=bookshelf)
		
	real_book_title = book.slug
	if real_book_title != book_title:
		return HttpResponseRedirect(reverse('libraries.views.profile_detail', args=[
			library_name, 
			bookshelf_slug, 
			book_isbn, 
			real_book_title
		]))
	else:
		return render_to_response('users/book_detail.html', {
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
			form = CreateCollectionForm(request.POST)
			if form.is_valid():
				form.save()
		else:
			form = CreateCollectionForm(collection_type=collection_type)
				
		return render_to_response('libraries/'+collection_type+'_form.html', {
			'form': form,
			'parent': request.GET.get('parent', None),
		})
	raise AssertionError, 'When instantiating a create_collection form the collection_type argument must be one fo the following: "library", "bookshelf" or "series".'