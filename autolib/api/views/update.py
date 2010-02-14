# api.views.update

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

def update_library(request):
	"""
	Update an existing Library Collection's following attributes:
		- Name
		- Description
	"""
	
	data = {'meta': {'success': False}}
		
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	library_pk = request.POST.get('library_pk', None) or request.POST.get('pk', None)
	
	name = request.POST.get('name', None) or request.POST.get('n', None)
	description = request.POST.get('description', None) or request.POST.get('d', None)
	
	error = False
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if library_pk is not None:
		
			try:
				library = Collection.objects.get(pk=library_pk, collection_type='library', owner=user)
				
				data['library'] = {}

				if name is not None:
					if re.match('^[a-zA-Z0-9\ \-\_]*$', name):
						library.name = name
						data['library']['name'] = library.name
					else:
						data['meta']['error'] = 'The Library name can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
						error = True
				
				if description is not None:
					library.description = description
					data['library']['description'] = library.description
				
				if not error:
					library = library.save()
					data['library']['last_modified'] = str(library.last_modified)
					data['meta']['success'] = True
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Library with that pk does not exist for this user"
				
		else:
			data['meta']['error'] = "library_pk was not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')



def update_bookshelf(request):
	"""
	Update an existing Bookshelf Collection's following attributes:
		- Name
		- Description
	"""
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	bookshelf_pk = request.POST.get('bookshelf_pk', None) or request.POST.get('pk', None)
	
	name = request.POST.get('name', None) or request.POST.get('n', None)
	description = request.POST.get('description', None) or request.POST.get('d', None)
	
	error = False
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if bookshelf_pk is not None:
		
			try:
				bookshelf = Collection.objects.get(pk=bookshelf_pk, collection_type='bookshelf', parent__owner=user)
				
				data['bookshelf'] = []
				
				try:
					if name is not None:
						if re.match('^[a-zA-Z0-9\ \-\_]*$', name):
							bookshelf.name = name
							data['bookshelf']['name'] = bookshelf.name
						else:
							data['meta']['error'] = 'The Bookshelf name can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
							error = True
					
					if description is not None:
						bookshelf.description = description
						data['bookshelf']['description'] = bookshelf.description
					
					if not error:
						bookshelf = bookshelf.save()
						data['bookshelf']['last_modified'] = str(bookshelf.last_modified)
						data['meta']['success'] = True
					
				except forms.ValidationError:
					data['meta']['error'] = "Validation Error"
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Bookshelf with that pk does not exist for this user"
				
		else:
			data['meta']['error'] = "bookshelf_pk was not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')


# Series
	
def update_series(request):
	"""
	Update an existing Series Collection's following attributes:
		- Name
		- Description
	"""
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	series_pk = request.POST.get('series_pk', None) or request.POST.get('pk', None)
	
	name = request.POST.get('name', None) or request.POST.get('n', None)
	description = request.POST.get('description', None) or request.POST.get('d', None)
	
	error = False
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if series_pk is not None:
		
			try:
				series = Collection.objects.get(pk=series_pk, collection_type='series', parent__parent__owner=user)
				
				data['series'] = []
				
				try:
					if name is not None:
						if re.match('^[a-zA-Z0-9\ \-\_]*$', name):
							series.name = name
							data['series']['name'] = series.name
						else:
							data['meta']['error'] = 'The Bookshelf name can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
							error = True
					
					if description is not None:
						series.description = description
						data['series']['description'] = series.description
					
					if not error:
						series = series.save()
						data['series']['last_modified'] = str(series.last_modified)
						data['meta']['success'] = True
					
				except forms.ValidationError:
					data['meta']['error'] = "Validation Error"
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Series with that pk does not exist for this user"
				
		else:
			data['meta']['error'] = "series_pk was not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')


# BookProfile

def update_profile(request):
	"""
	Update an existing BookProfile's following attributes:
		- Collection
	"""
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	profile_pk = request.POST.get('profile_pk', None) or request.POST.get('pk', None)
	
	collection_pk = request.POST.get('collection_pk', None) or request.POST.get('c_pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if profile_pk is not None:
		
			try:
				
				profile = BookProfile.objects.get(Q(pk=profile_pk) & (Q(collection__owner=user) | Q(collection__parent__owner=user) | Q(collection__parent__parent__owner=user)))
					
				if collection_pk is not None:
					
					try:
					
						collection = Collecion.objects.get(Q(pk=collection_pk) & (Q(owner=user) | Q(parent__owner=user) | Q(parent__parent__owner=user)))
						
						profile.collection = collection
						profile = profile.save()
						
						data['profile']['collection'] = profile.collection.pk
						data['profile']['last_modified'] = str(profile.last_modified)
						data['meta']['success'] = True
					
					except:
						data['meta']['error'] = "Collection with that pk does not exists for this user"
				
				else:
					data['meta']['error'] = "collection_pk not found"
				
			except BookProfile.DoesNotExist:
				data['meta']['error'] = "A BookProfile with that pk does not exist for this user"
				
		else:
			data['meta']['error'] = "series_pk was not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')