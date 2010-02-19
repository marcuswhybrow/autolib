# api.views.sync

from api import utils
from django.core import serializers
from django.db.models import Q
from base.models import Update
from datetime import datetime
import simplejson
from api.views import APIAuthView

class SyncUpdate(APIAuthView):
	def process(self, request):
		last_sync = request.POST.get('last_sync', None)
		if last_sync is not None:
			try:
				time = utils.parseDateTime(last_sync)
				updates = Update.objects.filter(user=self.user, time__gte=last_sync).order_by('-time')
				
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
				
				self.data['delete'] = []
				object_list = []
				
				for uuid,d in delete.items():
					self.data['delete'].append({
						'uuid': uuid,
						'object': d.object_type.split('.')[1],
						'time': str(d.time),
					})
				
				for uuid,u in update.items():
					object_list.append(u.get_object())
				
				self.data['update'] = simplejson.loads(serializers.serialize("json", object_list))
				
				for obj in self.data['update']:
					obj['model'] = obj['model'].split('.')[1]
					try:
						del obj['fields']['owner']
					except KeyError:
						pass
				
				object_list = []
				for uuid,i in insert.items():
					object_list.append(i.get_object())
				
				self.data['insert'] = simplejson.loads(serializers.serialize("json", object_list))
				
				for obj in self.data['insert']:
					obj['model'] = obj['model'].split('.')[1]
					try:
						del obj['fields']['owner']
					except KeyError:
						pass
				
				self.data['meta']['sync_time'] = str(datetime.now())
				self.data['meta']['success'] = True
			except ValueError:
				self.data['meta']['error'] = "last_sync was not in the format YYYY-MM-DD HH:MM:SS"
		else:
			self.data['meta']['error'] = "last_sync time not found"

sync_update = SyncUpdate()