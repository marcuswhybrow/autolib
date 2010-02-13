# api.views.auth

from django.contrib.auth.models import User

from django.contrib import auth
from django.contrib.sessions.models import Session

from libraries.models import Collection
from books.models import BookProfile

import api.utils
import re

from django.http import HttpResponse

from django.core import serializers

import simplejson

def auth_get_token(request):
	
	data = {'meta': {'success': False}}
	
	if request.user and request.user.is_authenticated():
		data['token_id'] = request.session._get_session_key()
		data['meta']['success'] = True
	else:
	
		username = request.POST.get('username', None) or request.POST.get('u', None)
		password = request.POST.get('password', None) or request.POST.get('p', None)
		
		if username is not None and password is not None:
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				
				data['token_id'] = request.session._get_session_key()
				
				data['meta']['success'] = True
		else:
			data['meta']['error'] = "Username and Password not supplied"
	
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def auth_destroy_token(request):
	
	data = {'meta': {'success': False}}
	
	token_id = request.POST.get('token_id', None) or request.POST.get('t', None)
	
	try:
		if token_id is not None:
			session = Session.objects.get(session_key=token_id)
		else:
			session = Session.objects.get(session_key=request.session._get_session_key())
		
		session.delete()
		data['meta']['success'] = True
			
	except Session.DoesNotExist:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')