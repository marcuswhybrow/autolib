# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from django.contrib import auth
from django.contrib.sessions.models import Session

from libraries.models import Collection

from books.models import BookProfile

import api.utils
import re

from django.http import HttpResponse

from django.core import serializers


### ---------
### Get Views
### ---------

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
		
		try:
			library = Collection.objects.get(pk=library_id, collection_type='library')
			
			if library.get_owner() == user:
				objects['name'] = library.name
				objects['description'] = library.description
				objects['url'] = library.get_absolute_url()
				objects['pk'] = library.pk
				objects['owner'] = library.owner
				
				objects['success'] = True
			else:
				objects['error'] = "You do not have permission to access this Library"
			
		except Collection.DoesNotExist:
			objects['error'] = "Library with that primary key does not exist"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')

def get_library_bookshelf_list(request, library_id):
	
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
			
			objects['success'] = True
		except Collection.DoesNotExist:
			objects['error'] = "Library with that primary key does not exist"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')

### Bookshelf stuff

def get_bookshelf_detail(request, bookshelf_id):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		try:
			bookshelf = Collection.objects.get(pk=bookshelf_id, collection_type='bookshelf')
			
			if bookshelf.get_owner() == user:
				objects['name'] = bookshelf.name
				objects['description'] = bookshelf.description
				objects['url'] = bookshelf.get_absolute_url()
				objects['pk'] = bookshelf.pk
				
				objects['success'] = True
			else:
				objects['error'] = "You do not have permission to access this Bookshelf"
			
		except Collection.DoesNotExist:
			objects['error'] = "Bookshelf with that primary key does not exist"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')

### Series Stuff

def get_series_list(request, bookshelf_id):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		try:
			bookshelf = Collection.objects.get(pk=bookshelf_id, collection_type='bookshelf')
			
			if bookshelf.get_owner() == user:
				
				object_lists['series'] = []
				for series in bookshelf.children.all():
					object_lists['series'].append({
						'name': series.name,
						'description': series.description,
						'pk': series.pk,
					})
				
				objects['success'] = True
			else:
				objects['error'] = "You do not have permission to access this Bookshelf"
			
		except Collection.DoesNotExist:
			objects['error'] = "Bookshelf with that primary key does not exist"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')
	
def get_series_detail(request, series_id):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		try:
			series = Collection.objects.get(pk=series_id, collection_type='series')
			
			if series.get_owner() == user:
				objects['name'] = series.name
				objects['description'] = series.description
				objects['pk'] = series.pk
				
				objects['success'] = True
			else:
				objects['error'] = "You do not have permission to access this Series"
			
		except Collection.DoesNotExist:
			objects['error'] = "Series with that primary key does not exist"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')
	
	
### BookProfile

def get_collection_book_profile_list(request):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	collection_id = request.GET.get('collection_id', None) or request.GET.get('c', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if collection_id is not None:
		
			try:
				collection = Collection.objects.get(pk=collection_id)
				
				if collection.get_owner() == user:
				
					object_lists['books'] = []
					for book in collection.books.all():
						object_lists['books'].append({
							'pk': book.pk,
							'isbn': book.book_instance.isbn,
							'title': book.book_instance.title,
							'description': book.book_instance.description,
							'author': book.book_instance.author,
							'publisher': book.book_instance.publisher,
							'published': book.book_instance.published,
						})
					objects['success'] = True
				else:
					objects['error'] = "You do not have permission to access this Collection"
						
			except Collection.DoesNotExist:
				objects['error'] = "Collection with that primary key does not exist"
		
		else:
			objects['error'] = "collection_id not found"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')

def get_book_profile_detail(request, book_profile_id):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		try:
			profile = BookProfile.objects.get(pk=book_profile_id)
			
			if profile.collection.get_owner() == user:
				
				objects['isbn'] = profile.book_instance.isbn
				objects['title'] = profile.book_instance.title
				objects['description'] = profile.book_instance.description
				objects['author'] = profile.book_instance.author
				objects['publisher'] = profile.book_instance.publisher
				objects['published'] = profile.book_instance.published
				
				objects['success'] = True
				
			else:
				objects['error'] = "You do not have permission to access this BookProfile"
							
		except BookProfile.DoesNotExist:
			objects['error'] = "BookProfile with that ID not found"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')


### ------------
### Insert Views
### ------------

from django import forms
from libraries.forms import CreateCollectionForm

def insert_library(request):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		try:
			form = CreateCollectionForm(request.POST)
			if form.is_valid():
				library = form.save(commit=False)
				library.collection_type='library'
				library.owner = user
				
				try:
					Collection.objects.get(name=library.name, owner=user, collection_type='library')
					objects['error'] = 'There is already a library of that name for this user!'
				except Collection.DoesNotExist:
					library.save()
					objects['name'] = library.name
					objects['description'] = library.description
					objects['owner'] = library.owner
					objects['url'] = library.get_absolute_url()
					
					objects['success'] = True
			else:
				objects['error'] = "There was a validation error"
			
		except forms.ValidationError:
			objects['error'] = "Validation Error"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')
	
def insert_bookshelf(request):
	pass

def insert_series(request):
	pass

def insert_book(request):
	pass

### ------------
### Update Views
### ------------

def update_library(request):
	
	objects = {'success': False}
	object_lists = {}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	library_id = request.POST.get('library_id', None) or request.POST.get('l', None) or request.POST.get('id', None)
	
	name = request.POST.get('name', None) or request.POST.get('n', None)
	description = request.POST.get('description', None) or request.POST.get('d', None)
	
	error = False
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if library_id is not None:
		
			try:
				library = Collection.objects.get(pk=library_id, collection_type='library')
				
				try:
					if name is not None:
						if re.match('^[a-zA-Z0-9\ \-\_]*$', name):
							library.name = name
							objects['name'] = library.name
						else:
							objects['error'] = 'The Library name can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
							error = True
					
					if description is not None:
						library.description = description
						objects['description'] = library.description
					
					if not error:
						library.save()
						objects['success'] = True
					
				except forms.ValidationError:
					objects['error'] = "Validation Error"
				
			except Collection.DoesNotExist:
				objects['error'] = "A Library with that id does not exist"
				
		else:
			objects['error'] = "library_id was not found"
		
	else:
		objects['error'] = "Invalid token"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')

def update_bookshelf(request):
	pass
	
def update_series(request):
	pass

### ----------
### Sync Views
### ----------

from datetime import datetime

from books.models import Book, BookProfile

from base.models import Update

from django.db.models import Q

from django.core import serializers
import simplejson

def sync_update(request):
	
	
	json = {'success': False}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	last_sync = request.GET.get('last_sync', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if last_sync is not None:
			
			try:
				time = utils.parseDateTime(last_sync)
				
				updates = Update.objects.filter(user=user, time__gte=last_sync).order_by('-time')
				
				delete = {}
				update = {}
				insert = {}
				
				for u in updates:
					if u.action == 'delete':
						delete[u.uuid] = u
					elif u.action == 'update':
						if u.uuid not in delete:
							update[u.uuid] = u
					elif u.action == 'insert':
						try:
							del delete[u.uuid]
						except KeyError:
							try:
								del update[u.uuid]
							except KeyError:
								pass
							insert[u.uuid] = u
							
				print delete
				print update
				print insert
				
				json['delete'] = []
				object_list = []
				
				for uuid,d in delete.items():
					json['delete'].append({
						'uuid': uuid,
						'object': d.object_type.split('.')[1],
						'time': str(d.time),
					})
				
				for uuid,u in update.items():
					object_list.append(u.get_object())
				
				json['update'] = simplejson.loads(serializers.serialize("json", object_list))
				
				object_list = []
				for uuid,i in insert.items():
					object_list.append(i.get_object())
				
				json['insert'] = simplejson.loads(serializers.serialize("json", object_list))
				
				json['sync_time'] = str(datetime.now())
				json['success'] = True

			except ValueError:
				json['error'] = "last_sync was not in the format YYYY-MM-DD HH:MM:SS"
			
		else:
			json['error'] = "last_sync time not found"
			
	else:
		json['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(json), mimetype='application/json')
		
# 	return render_to_response('api/serialiser.html',{
# 		'object_lists': object_lists,
# 		'objects': objects,
# 	}, mimetype='application/json')


### ----------
### Auth Views
### ----------

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