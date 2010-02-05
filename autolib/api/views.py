# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from django.contrib import auth
from django.contrib.sessions.models import Session

from libraries.models import Collection

import utils

from django.http import HttpResponse

from django.core import serializers

### Library stuff

def get_library_list(request):

	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		object_lists['libraries'] = []
		for library in user.libraries.all():
			object_lists['libraries'].append({
				'pk': library.pk,
				'name': library.name,
				'description': library.description,
				'url': library.get_absolute_url(),
			})
		objects['success'] = True
	else:
		objects['error'] = "Invalid token"
	
	#return HttpResponse(serializers.serialize('json', user.libraries.all()))
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')

def get_library_detail(request, library_id):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		object_lists['books'] = []
		try:
			library = COllection.objects.get(pk=library_id, collection_type='library')
			for book in library.books.all():
				object_lists['books'].append({
					'pk': book.pk,
					'isbn': book.book_instance.isbn,
					'title': book.book_instance.title,
					'description': book.book_instance.description,
					'author': book.book_instance.author,
					'publisher': book.book_instance.publisher,
					'published': book.book_instance.published,
				})
		except Collection.DoesNotExist:
			objects['error'] = "Library with that primary key does not exist"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')

def get_library_book_list(request, library_id):
	pass

### Bookshelf stuff
	
def get_bookshelf_list(request, library_id):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		try:
			library = Collection.objects.get(pk=library_id, collection_type='library')
			object_lists['bookshelves'] = []
			for bookshelf in library.children.all():
				object_lists['bookshelves'].append({
					'pk': library.pk,
					'name': library.name,
					'description': library.description,
					'url': library.get_absolute_url(),
				})
				
			objects['name'] = library.name
			objects['description'] = library.description
			objects['pk'] = library.pk
			objects['url'] = library.get_absolute_url()
			
			objects['success'] = True
		except Collection.DoesNotExist:
			objects['error'] = "Library with that primary key does not exist"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')

def get_bookshelf_detail(request, bookshelf_id):
	pass
	
def get_bookshelf_book_list(request, bookshelf_id):
	pass

### Series Stuff

def get_series_list(request, bookshelf_id):
	pass
	
def get_series_detail(request, series_id):
	pass

def get_series_book_list(request, series_id):
	pass



### Auth Methods

def auth_get_token(request):
	
	objects = {'success': False}
	object_lists = {}
	
	if request.user and request.user.is_authenticated():
		objects['token_id'] = request.session._get_session_key()
		objects['success'] = True
	else:
	
		username = request.GET.get('username', None) or request.GET.get('u', None)
		password = request.GET.get('password', None) or request.GET.get('p', None)
		
		if username is not None and password is not None:
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				
				objects['token_id'] = request.session._get_session_key()
				
				objects['success'] = True
		else:
			objects['error'] = "Username and Password not supplied"
	
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')


def auth_destroy_token(request):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	try:
		if token_id is not None:
			session = Session.objects.get(session_key=token_id)
		else:
			session = Session.objects.get(session_key=request.session._get_session_key())
		
		session.delete()
		objects['success'] = True
			
	except Session.DoesNotExist:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')


def test(request):
	return HttpResponse('test')