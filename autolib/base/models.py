from django.db import models

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
	object_type = models.CharField(max_length=200)
	
	def __unicode__(self):
		return '%s - %s - %s' % (self.action, self.object_type, self.user)
	
	def get_object(self):
		try:
			return models.get_model(*self.object_type.split('.')).objects.get(pk=self.uuid)
		except ObjectDoesNotExist:
			print self
			return None

# class Syncable(models.Model):
# 	
# 	# The time the object was INSERTed
# 	added = models.DateTimeField(auto_now_add=True)
# 	# The last time the object was UPDATEd
# 	last_modified = models.DateTimeField(auto_now=True)
# 	
# 	class Meta:
# 		abstract = True
# 	
# 	def get_owner(self):
# 		raise NotImplementedError
# 	
# 	def save(self, *args, **kwargs):
# 		
# 		# Determin INSERT of UPDATE via UUID presence
# 		if not self.pk:
# 			action = 'insert'
# 		else:
# 			action = 'update'
# 		
# 		# do the rest of save as normal and log the insert in update
# 		super(Syncable, self).save(*args, **kwargs)
# 		
# 		Update(uuid=self.pk, object_type=self.__module__.split('.')[0] + '.' + self.__class__.__name__, action=action).save()
# 	
# 	def delete(self, *args, **kwargs):
# 				
# 		Update(uuid=self.pk, object_type=self.__module__.split('.')[0] + '.' + self.__class__.__name__, action='delete', user=self.get_owner()).save()
# 		super(Syncable, self).delete(*args, **kwargs)

from uuid import uuid4

class UUIDSyncable(models.Model):
	
	# The time the object was INSERTed
	added = models.DateTimeField(auto_now_add=True)
	# The last time the object was UPDATEd
	last_modified = models.DateTimeField(auto_now=True)
	# UUIDSyncable objects must have a UUID as their primary key
	uuid = models.CharField(primary_key=True, max_length=64, editable=False, blank=True)
	
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
		Update(uuid=self.pk, object_type=self.__module__.split('.')[0] + '.' + self.__class__.__name__, action=action, user=self.get_owner()).save()
	
	def delete(self, *args, **kwargs):
				
		Update(uuid=self.pk, object_type=self.__module__.split('.')[0] + '.' + self.__class__.__name__, action='delete', user=self.get_owner()).save()
		super(UUIDSyncable, self).delete(*args, **kwargs)