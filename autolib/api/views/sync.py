# api.views.sync

from base import utils
from django.core import serializers
from django.db.models import Q
from base.models import Update
from datetime import datetime
import simplejson
from api.views import APIAuthView

class SyncUpdate(APIAuthView):

	INITIAL_SYNC_TYPE = 'initial'
	INCREMENTAL_SYNC_TYPE = 'incremental'
	
	def process(self, request):
		"""
		Gets the changes to the database which have occurred since a 'last_sync' time for the authenticated user,
		
		Using the following logic to eliminate redundant sync actions:
			- If an object was inserted and deleted, there is no need to tell the client.
			- A client only needs the most recent update for any one object (but still requires the initial insert)
		"""
		
		# Get the POST variables needed
		sync_type = request.POST.get('type', None)
		
		if sync_type is not None:
			# If sync_type was supplied
			
			if sync_type == self.INITIAL_SYNC_TYPE:
				# If its and initial sync
				# Get all updates for the user
				updates = Update.objects.filter(user=self.user).order_by('-time')
				
			elif sync_type == self.INCREMENTAL_SYNC_TYPE:
				# If its an incremental sync
				
				# Get the incremental updates
				updates = self._incremental_update(request)
				
			else:
				self.data['meta']['error'] = 'Sync type not valid, must be %s or %s' % (self.INITIAL_SYNC_TYPE, self.INCREMENTAL_SYNC_TYPE)
				return
			
		else:
			# sync_type not supplied
			
			# Get the incremental updates
			updates = self._incremental_update(request)
		
		# Filter updates
		if updates is not None:
			self._filter_updates(updates)
		else:
			return
			
	def _incremental_update(self, request):
		
		# Get the time of the last sync
		last_sync = request.POST.get('last_sync', None)
		
		if last_sync is not None:
			# If last_sync was in the POST data
			
			try:
				# Convert the last time the client synced with the database into DateTime
				time = utils.parseDateTime(last_sync)
				
			except ValueError:
				# If the conversion failed
				self.data['meta']['error'] = "last_sync was not in the format YYYY-MM-DD HH:MM:SS"
				return None
				
			else:
				# If the conversion was successfull
				
				# Get all updates for the current user since that time
				return Update.objects.filter(user=self.user, time__gte=last_sync).order_by('-time')
				
		else:
			# If the last sync time was not found, return an error
			self.data['meta']['error'] = "last_sync time not found"
			return
	
	def _filter_updates(self, updates):
		# Dictionaries to whitle down the objects which need to be synced
		delete, update, insert = {}, {}, {}
		
		for u in updates:
			# For all updates
			
			if u.content_object is None:
				# If the object has been deleted (which it shouldn't have been)
				# Delete the update referencing it
				u.delete()
				continue
				
			if u.action == 'delete':
				# If it's a delete Update
				# Add it to the delete dictionary
				delete[u.object_pk] = u
				
			elif u.action == 'update':
				# If it's an update Update
				if u.object_pk not in delete:
					# And has not been deleted
					# Add it to the update dictionary
					update[u.object_pk] = u
					
			elif u.action == 'insert':
				# If it's an insert Update
				
				try:
					# Try and remove the delete Update (and don't put it in the insert dictionary)
					del delete[u.object_pk]
					
				except KeyError:
					# If exception, it wasn't in the delete dictionary
					
					try:
						# Try and remove the update Update
						del update[u.object_pk]
						
					except KeyError:
						# If exception, it wasn't in the update dictionary
						pass
					
					# Add it to the insert dictionary
					insert[u.object_pk] = u
		
		# Build a list of the objects to delete
		object_list = []
		for pk,u in delete.items():
			if u.content_object is not None:
				object_list.append(u.content_object)
				
		print object_list
		
		# Serialise the objects to delete
		self.data['delete'] = simplejson.loads(serializers.serialize("json", object_list))
		
		# Build a list of objects to update
		object_list = []
		for pk,u in update.items():
			if u.content_object is not None:
				object_list.append(u.content_object)
		
		# Serialise the objects to update
		self.data['update'] = simplejson.loads(serializers.serialize("json", object_list))
		
		# Build a list of the objects to insert
		object_list = []
		for pk,i in insert.items():
			if i.content_object is not None:
				object_list.append(i.content_object)
		
		# Serialise the objects to insert
		self.data['insert'] = simplejson.loads(serializers.serialize("json", object_list))
		
		# Remove the owner and is_deleted fields from all serliased objects
		for obj in list(self.data['insert'] + self.data['update'] + self.data['delete']):
			obj['model'] = obj['model'].split('.')[1]
			try:
				del obj['fields']['owner']
				del obj['fields']['is_deleted']
			except KeyError:
				pass
		
		# Set the time for this sync as now
		self.data['meta']['sync_time'] = str(datetime.now())
		# The request was processed successfully
		self.data['meta']['success'] = True

# Bind an instance of this class to a referenceable name
sync_update = SyncUpdate()