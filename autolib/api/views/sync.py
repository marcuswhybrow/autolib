# api.views.sync

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



from datetime import datetime

from books.models import Book, BookProfile

from base.models import Update

from django.db.models import Q

from django.core import serializers
import simplejson

def sync_update(request):
	
	
	data = {'meta': {'success': False}}
	
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
				
				data['delete'] = []
				object_list = []
				
				for uuid,d in delete.items():
					data['delete'].append({
						'uuid': uuid,
						'object': d.object_type.split('.')[1],
						'time': str(d.time),
					})
				
				for uuid,u in update.items():
					object_list.append(u.get_object())
				
				data['update'] = simplejson.loads(serializers.serialize("json", object_list))
				
				for obj in data['update']:
					obj['model'] = obj['model'].split('.')[1]
					try:
						del obj['fields']['owner']
					except KeyError:
						pass
				
				object_list = []
				for uuid,i in insert.items():
					object_list.append(i.get_object())
				
				data['insert'] = simplejson.loads(serializers.serialize("json", object_list))
				
				for obj in data['insert']:
					obj['model'] = obj['model'].split('.')[1]
					try:
						del obj['fields']['owner']
					except KeyError:
						pass
				
				data['meta']['sync_time'] = str(datetime.now())
				data['meta']['success'] = True

			except ValueError:
				data['meta']['error'] = "last_sync was not in the format YYYY-MM-DD HH:MM:SS"
			
		else:
			data['meta']['error'] = "last_sync time not found"
			
	else:
		data['meta']['error'] = "Invalid token"
	
	return HttpResponse(simplejson.dumps(data), mimetype='application/json')