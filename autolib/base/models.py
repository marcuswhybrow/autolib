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
	
	uuid = models.CharField(max_length=64)
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
	
	# The time the object was INSERTed
	added = models.DateTimeField(auto_now_add=True)
	
	# The last time the object was UPDATEd
	last_modified = models.DateTimeField(auto_now=True)
	
	# UUIDSyncable objects must have a UUID as their primary key
	uuid = models.CharField(primary_key=True, max_length=64, editable=False, blank=True)
	
	# The updates this syncable item is related to
	updates = generic.GenericRelation(Update)
	
	# Flag to specify that the object is deleted (instead of actual deletion)
	isDeleted = models.BooleanField(default=False)
	
	objects = UUIDSyncableManager()
	all_objects = models.Manager()
	deleted = UUIDSyncableDeletedManager()
	
	class Meta:
		# Objects may only extend this class
		abstract = True
	
	def get_owner(self):
		raise NotImplementedError
	
	def save(self, *args, **kwargs):
		
		# If not UUID specified Assign a random UUID
		if not self.pk:
			self.pk = str(uuid4())
			action = 'insert'
		else:
			action = 'update'
		
		# Call the rest of save normally
		super(UUIDSyncable, self).save(*args, **kwargs)
		Update(uuid=self.pk, content_object=self, action=action, user=self.get_owner()).save()
	
	def delete(self, delete_from_db=False, *args, **kwargs):
		
		if delete_from_db:
			super(UUIDSyncable, self).delete(*args, **kwargs)
		else:
			# Flag the object as deleted
			self.deleted = True
			super(UUIDSyncable, self).save(*args, **kwargs)
			
			# Create a delete update		
			Update(uuid=self.pk, content_object=self, action='delete', user=self.get_owner()).save()
				
		