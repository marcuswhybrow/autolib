# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from django.contrib import auth
from django.contrib.sessions.models import Session

import utils

from django.http import HttpResponse

def get_libraries(request):

	objects = {'success': False}
	object_lists = {}
	
	token_id = request.GET.get('token_id', None) or request.GET.get('t', None)
	
	if token_id is not None:
		
		user = utils.get_user_from_token(token_id)
			
		if user:
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
	
	else:
		objects['error'] = "No token found"
	
	return render_to_response('api/serialiser.html',{
		'object_lists': object_lists,
		'objects': objects,
	}, mimetype='application/json')


def auth_get_token(request):
	
	objects = {'success': False}
	object_lists = {}
	
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
	
	if token_id is not None:
		try:
			session = Session.objects.get(session_key=token_id)
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