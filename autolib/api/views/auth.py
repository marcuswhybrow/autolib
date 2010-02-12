# api.views.auth

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