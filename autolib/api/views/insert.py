# api.views.insert

from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from django.contrib import auth
from django.contrib.sessions.models import Session

from libraries.models import Collection

from books.models import BookProfile

from api import utils
import re

from django.http import HttpResponse

from django.core import serializers

from django import forms
from libraries.forms import CreateCollectionForm

import simplejson

from django.db import IntegrityError

def insert_library(request):
	
	data = {'meta': {'success': False}}
	
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
					data['meta']['error'] = 'There is already a library of that name for this user!'
				except Collection.DoesNotExist:
					library.save()
					data['library'] = {}
					data['library']['pk'] = library.pk
					data['library']['name'] = library.name
					data['library']['description'] = library.description
					data['library']['url'] = library.get_absolute_url()
					
					data['meta']['success'] = True
			else:
				data['meta']['error'] = "There was a validation error"
			
		except forms.ValidationError:
			data['meta']['error'] = "Validation Error"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')
	
def insert_bookshelf(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	parent_pk = request.POST.get('parent', None) or request.GET.get('p', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if parent_pk is not None:
			
			try: # Collection get
				
				try: # Validation errors
					
					try: # save new collection
					
						form = CreateCollectionForm(request.POST)
						if form.is_valid():
							bookshelf = form.save(commit=False)
							bookshelf.collection_type='bookshelf'
							bookshelf.parent = Collection.objects.get(pk=parent_pk, collection_type='library', owner=user)

							bookshelf.save()
							data['bookshelf'] = {}
							data['bookshelf']['name'] = bookshelf.name
							data['bookshelf']['description'] = bookshelf.description
							data['bookshelf']['url'] = bookshelf.get_absolute_url()
							data['bookshelf']['pk'] = bookshelf.pk
							data['bookshelf']['parent'] = bookshelf.parent.pk
							
							data['meta']['success'] = True
						
						else:
							data['meta']['error'] = "There was a validation error"
						
					except IntegrityError:
						data['meta']['error'] = "A Bookshelf of that name in this Library already exists for this User"
					
				except forms.ValidationError:
					data['meta']['error'] = "Validation Error"
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "parent library does not exist"
		
		else:
			data['meta']['error'] = "parent was not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def insert_series(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	parent_pk = request.POST.get('parent', None) or request.GET.get('p', None)
	
	if token_id is not None:
		user = utils.get_user_from_token(token_id)
	else:
		user = request.user
	
	if user and user.is_authenticated():
		
		if parent_pk is not None:
			
			try: # Collection get
				
				try: # Validation errors
					
					try: # save new collection
					
						form = CreateCollectionForm(request.POST)
						if form.is_valid():
							series = form.save(commit=False)
							series.collection_type='series'
							series.parent = Collection.objects.get(pk=parent_pk, collection_type='bookshelf', parent__owner=user)

							series.save()
							data['series'] = {}
							data['series']['name'] = series.name
							data['series']['description'] = series.description
							data['series']['pk'] = series.pk
							data['series']['parent'] = series.parent.pk
							
							data['meta']['success'] = True
						
						else:
							data['meta']['error'] = "There was a validation error"
						
					except IntegrityError:
						data['meta']['error'] = "A Series of that name in this Bookshelf already exists for this User"
					
				except forms.ValidationError:
					data['meta']['error'] = "Validation Error"
				
			except Collection.DoesNotExist:
				data['meta']['error'] = "parent Bookshelf does not exist"
		
		else:
			data['meta']['error'] = "parent was not found"
		
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def insert_book(request):
	pass