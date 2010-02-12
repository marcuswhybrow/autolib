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
	
	data = {}
	data['meta']['success'] = False
	
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
		
		if library_id is not None:
		
			try:
				library = Collection.objects.get(pk=library_pk, collection_type='library', owner=user)
				
				data['library'] = []
				
				try:
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
						library.save()
						data['meta']['success'] = True
					
				except forms.ValidationError:
					data['meta']['error'] = "Validation Error"
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Library with that pk does not exist"
				
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
	
	data = {}
	data['meta']['success'] = False
	
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
		
		if library_id is not None:
		
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
						bookshelf.save()
						data['meta']['success'] = True
					
				except forms.ValidationError:
					data['meta']['error'] = "Validation Error"
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Bookshelf with that pk does not exist"
				
		else:
			data['meta']['error'] = "bookshelf_pk was not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	
def update_series(request):
	pass