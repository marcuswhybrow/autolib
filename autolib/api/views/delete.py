from django.http import HttpResponse
from api import utils

from books.models import BookProfile
from libraries.models import Collection

import simplejson

# Library

def delete_library(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	library_pk = request.GET.get('library_pk', None) or request.GET.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if library_pk is not None:
			
			try:
				
				library = Collection.objects.get(pk=library_pk, owner=user, collection_type='library')
				
				if not library.children.all():
					
					if not library.books.all():
						
						data['library'] = {
							'pk': library.pk
						}
						library.delete()
						data['meta']['success'] = True
						
					else:
						data['meta']['error'] = "This Library cannot be deleted as it contains books"
					
				else:
					data['meta']['error'] = "This Library cannot be deleted as it contains Bookshelves (other than the unsorted bin)"
			
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Library Collection with that pk does not exist for this user"
			
		else:
			data['meta']['error'] = "library_pk not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# Bookshelf

def delete_bookshelf(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	bookshelf_pk = request.GET.get('bookshelf_pk', None) or request.GET.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if bookshelf_pk is not None:
			
			try:
				
				bookshelf = Collecion.objects.get(pk=bookshelf_pk, parent__owner=user, collection_type='bookshelf')
				
				if not bookshelf.children.all():
					
					if not bookshelf.books.all():
						
						data['bookshelf'] = {
							'pk': bookshelf.pk
						}
						bookshelf.delete()
						data['meta']['success'] = True
						
					else:
						data['meta']['error'] = "This Bookshelf cannot be deleted as it contains books"
					
				else:
					data['meta']['error'] = "This Bookshelf cannot be deleted as it contains Series"
			
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Bookshelf Collection with that pk does not exist for this user"
			
		else:
			data['meta']['error'] = "bookshelf_pk not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# Series

def delete_series(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	series_pk = request.GET.get('series_pk', None) or request.GET.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if series_pk is not None:
			
			try:
				
				series = Collecion.objects.get(pk=series_pk, parent__parent__owner=user, collection_type='series')
				
				if not series.children.all():
					
					if not series.books.all():
						
						data['series'] = {
							'pk': series.pk
						}
						series.delete()
						data['meta']['success'] = True
						
					else:
						data['meta']['error'] = "This Series cannot be deleted as it contains books"
					
				else:
					data['meta']['error'] = "This Series cannot be deleted as it has children Collection's (which should never happen)"
			
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Series Collection with that pk does not exist for this user"
			
		else:
			data['meta']['error'] = "series_pk not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

# BookProfile

from django.db.models import Q

def delete_profile(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	profile_pk = request.GET.get('profile_pk', None) or request.GET.get('pk', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if profile_pk is not None:
			
			try:
				
				profile = BookProfile.objects.get(Q(pk=profile_pk) & (Q(collection__owner=user) | Q(collection__parent__owner=user) | Q(collection__parent__parent__owner=user)))
						
				data['profile'] = {
					'pk': series.pk
				}
				profile.delete()
				data['meta']['success'] = True
			
			except Collection.DoesNotExist:
				data['meta']['error'] = "A Profile with that pk does not exist for this user"
			
		else:
			data['meta']['error'] = "profile_pk not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')