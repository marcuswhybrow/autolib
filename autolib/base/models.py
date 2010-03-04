from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class Config(models.Model):
	'''
	System-wide configuration, key value pairs (with slug) which allow important 
	values such as naming schemes to be altered later on.
	'''
	
	key = models.CharField(max_length=200, primary_key=True)
	value = models.CharField(max_length=200)
	slug = models.SlugField()
	
	def __unicode__(self):
		return '%s : %s' % (self.key, self.value)
		

UPDATE_TYPES = (
	('insert', 'Insert'),
	('update', 'Update'),
	('delete', 'Delete'),
)

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Update(models.Model):
	"""
	
	"""
	
	time = models.DateTimeField(auto_now_add=True, db_index=True)
	action = models.CharField(max_length=20, choices=UPDATE_TYPES)
	user = models.ForeignKey(User, related_name="updates", editable=False, db_index=True, null=True, blank=True)
	
	content_type = models.ForeignKey(ContentType)
	object_pk = models.CharField(max_length=64)
	content_object = generic.GenericForeignKey('content_type', 'object_pk')
	
	def __unicode__(self):
		return '%s - %s - %s - %s' % (self.action, self.content_type, self.content_object, self.user)

from uuid import uuid4
from base.managers import UUIDSyncableManager, UUIDSyncableDeletedManager

class UUIDSyncable(models.Model):
	"""
	A class which extends for UUIDSyncable will have its insertions, updates and deletions recorded.
	The updates can then be synced to client databases using the API app.
	"""
	
	# The time the object was INSERTed
	added = models.DateTimeField(auto_now_add=True)
	
	# The last time the object was UPDATEd
	last_modified = models.DateTimeField(auto_now=True)
	
	# UUIDSyncable objects must have a UUID as their primary key
	uuid = models.CharField(primary_key=True, max_length=64, editable=False, blank=True)
	
	# The updates this syncable item is related to
	updates = generic.GenericRelation(Update, content_type_field='content_type', object_id_field='object_pk')
	
	# Flag to specify that the object is deleted (instead of actual deletion)
	is_deleted = models.BooleanField(default=False, editable=False)
	
	# Since the default manager is not called objects,
	# all bespoke code uses Model.objects.all() to get all objects for a model (which is no longer the default manager)
	# But behind the scenes django modules use Model._default_manager.all(), which uses Model.all_objects.all()
	# as it is the new default manager
	all_objects = models.Manager()
	objects = UUIDSyncableManager()
	deleted = UUIDSyncableDeletedManager()
	
	class Meta:
		# Objects may only extend this class
		abstract = True
	
	def get_owner(self):
		raise NotImplementedError
	
	def save(self, *args, **kwargs):
		"""
		Saves the objects and adds an either an 'insert' or 'update' Update
		"""
		
		# If not UUID specified Assign a random UUID
		if not self.pk:
			self.pk = str(uuid4())
			action = 'insert'
		else:
			action = 'update'
		
		# Call the rest of save normally
		super(UUIDSyncable, self).save(*args, **kwargs)
		Update(content_object=self, action=action, user=self.get_owner()).save()
	
	def delete(self, delete_from_db=False, *args, **kwargs):
		"""
		Soft deletes the object such that it remains in the database but is not picked up by the 'objects' manager
		Deleted objects can be found using the 'deleted' manager or the 'all_objects' manager
		
		If delete_from_db is True, the object is hard deleted fromt he database and all references w
		"""
		
		if delete_from_db is True:
			# Delete all updates which reference this object
			self.updates.all().delete()
			# Delete the object
			super(UUIDSyncable, self).delete(*args, **kwargs)
		else:
			# Flag the object as deleted
			self.is_deleted = True
			super(UUIDSyncable, self).save(*args, **kwargs)
			
			# Create a delete update		
			Update(content_object=self, action='delete', user=self.get_owner()).save()