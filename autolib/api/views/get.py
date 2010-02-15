# api.views.get

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

import simplejson

# Library

def get_library_list(request):
	"""
	Gets the library list for the current request.user (or user token)
	"""

	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		data['libraries'] = []
		for library in user.libraries.all():
			data['libraries'].append({
				'pk': library.pk,
				'name': library.name,
				'slug': library.slug,
				'description': library.description,
				'url': library.get_absolute_url(),
				'added': str(library.added),
				'last_modified': str(library.last_modified),
			})
		data['meta']['success'] = True
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def get_library_detail(request):
	"""
	Gets details regarding a single library, which must be owned by the current request.user (or user token)
	"""
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	library_pk = request.POST.get('library_pk', None) or request.POST.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if library_pk is not None:
			
			try:
				library = Collection.objects.get(pk=library_pk, collection_type='library', owner=user)
				data['library'] = {
					'pk': library.pk,
					'name': library.name,
					'description': library.description,
					'url': library.get_absolute_url(),
					'slug': library.slug,
					'added': str(library.added),
					'last_modified': str(library.last_modified),
				}
				
				data['meta']['success'] = True
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "Library not found with that pk, for that user"
			
		else:
			data['meta']['error'] = "library_pk not found"
		
	else:
		objects['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# Bookshelf

def get_bookshelf_list(request):
	"""
	Gets the list of bookshelves for a given library collection,
	such that the library must be owned by the current request.user (or request token)
	"""
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	library_pk = request.POST.get('library_pk', None) or request.POST.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if library_pk is not None:
			
			try:
				library = Collection.objects.get(pk=library_pk, collection_type='library', owner=user)
				data['bookshelves'] = []
				
				for bookshelf in library.children.all():
					data['bookshelves'].append({
						'pk': bookshelf.pk,
						'name': bookshelf.name,
						'parent': bookshelf.parent.pk,
						'slug': bookshelf.slug,
						'description': bookshelf.description,
						'url': bookshelf.get_absolute_url(),
						'added': str(bookshelf.added),
						'last_modified': str(bookshelf.last_modified),
					})
				
				data['meta']['success'] = True
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "Library not found with that pk, for that user"
			
		else:
			data['meta']['error'] = "library_pk not found"
		
	else:
		objects['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def get_bookshelf_detail(request):
	"""
	Gets details regarding a single bookshelf, such that the parent library
	must be owned by the current request.user (or user token)
	"""
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	bookshelf_pk = request.POST.get('bookshelf_pk', None) or request.POST.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if bookshelf_pk is not None:
			
			try:
				bookshelf = Collection.objects.get(pk=bookshelf_pk, collection_type='bookshelf', parent__owner=user)
				data['bookshelf'] = {
					'pk': bookshelf.pk,
					'name': bookshelf.name,
					'parent': bookshelf.parent.pk,
					'description': bookshelf.description,
					'url': bookshelf.get_absolute_url(),
					'slug': bookshelf.slug,
					'added': str(bookshelf.added),
					'last_modified': str(bookshelf.last_modified),
				}
				
				data['meta']['success'] = True
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "Bookshelf not found with that pk, for that user"
			
		else:
			data['meta']['error'] = "bookshelf_pk not found"
		
	else:
		objects['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# Series

def get_series_list(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	bookshelf_pk = request.POST.get('bookshelf_pk', None) or request.POST.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if bookshelf_pk is not None:
			
			try:
				bookshelf = Collection.objects.get(pk=bookshelf_pk, collection_type='bookshelf', parent__owner=user)
				data['series'] = []
				
				for series in bookshelf.children.all():
					data['series'].append({
						'pk': series.pk,
						'name': series.name,
						'parent': series.parent.pk,
						'slug': series.slug,
						'description': series.description,
						'added': str(series.added),
						'last_modified': str(series.last_modified),
					})
				
				data['meta']['success'] = True
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "Bookshelf not found with that pk, within that Library for this user"
			
		else:
			data['meta']['error'] = "bookshelf_pk not found"
		
	else:
		objects['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	

def get_series_detail(request):
	"""
	Gets details regarding a single series, such that the parent bookshelves parent library
	must be owned by the current request.user (or user token)
	"""
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	series_pk = request.POST.get('series_pk', None) or request.POST.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if series_pk is not None:
			
			try:
				series = Collection.objects.get(pk=series_pk, collection_type='series', parent__parent__owner=user)
				data['series'] = {
					'pk': series.pk,
					'name': series.name,
					'parent': series.parent.pk,
					'description': series.description,
					'slug': series.slug,
					'added': str(series.added),
					'last_modified': str(series.last_modified),
				}
				
				data['meta']['success'] = True
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "Series not found with that pk, for that user"
			
		else:
			data['meta']['error'] = "series_pk not found"
		
	else:
		objects['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	
	
# BookProfile

from django.db.models import Q

def get_profile_list(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	collection_id = request.POST.get('collection_pk', None) or request.POST.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if collection_id is not None:
		
			try:
				collection = Collection.objects.get(Q(pk=collection_id) & (Q(owner=user) | Q(parent__owner=user) | Q(parent__parent__owner=user)))
				
				data['profiles'] = []
				for profile in collection.books.all():
					data['profiles'].append({
						'collection': profile.collection.pk,
						'book': profile.book_instance.pk,
						'added': str(profile.added),
						'last_modified': str(profile.last_modified),
					})
				data['meta']['success'] = True
						
			except Collection.DoesNotExist:
				data['meta']['error'] = "Collection with that primary key does not exist, for this user"
		
		else:
			data['meta']['error'] = "collection_pk not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def get_profile_detail(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	profile_pk = request.POST.get('profile_pk', None) or request.POST.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if profile_pk is not None:
		
			try:
				profile = BookProfile.objects.get(Q(pk=profile_pk) & (Q(collection__owner=user) | Q(collection__parent__owner=user) | Q(collection__parent__parent__owner=user)))
				
				data['profile'] = {
					'pk': profile.book_instance.pk,
					'isbn': profile.book_instance.isbn,
					'title': profile.book_instance.title,
					'author': profile.book_instance.author,
					'published': profile.book_instance.published,
					'publisher': profile.book_instance.publisher,
					'description': profile.book_instance.description,
					'collection': profile.collection.pk,
					'added': profile.added,
					'last_modified': profile.last_modified,
				}
				data['meta']['success'] = True
						
			except BookProfile.DoesNotExist:
				data['meta']['error'] = "BookProfile with that primary key does not exist, for this user"
		
		else:
			data['meta']['error'] = "profile_pk not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')