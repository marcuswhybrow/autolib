# Allows classes to extend the models amd forms classes.
from django.db import models
from django.db.models import permalink
from django import forms

# Allows referencing the user.
from django.contrib.auth.models import User
from django.utils.http import urlquote_plus
import managers
import re

from django.core.exceptions import ValidationError
from django.db.models import Q

import threading

#########################
### Collections Model ###
#########################

COLLECTION_TYPE_CHOICES = (
	('library', 'Library'),
	('bookshelf', 'Book Shelf'),
	('series', 'Series'),
)

from base.models import UUIDSyncable
from django.template.defaultfilters import slugify

class Collection(UUIDSyncable):
	
	name = models.CharField(max_length=100)
	collection_type = models.CharField(max_length=20, choices=COLLECTION_TYPE_CHOICES)
	description = models.TextField(null=True, blank=True)
	parent = models.ForeignKey('self', related_name="children", null=True, blank=True)
	owner = models.ForeignKey(User, related_name="libraries", null=True, blank=True)
	slug = models.CharField(max_length=100, editable=False)
	
	def get_user(self):
		if self.collection_type == 'library':
			return self.owner
		elif self.collection_type == 'bookshelf':
			return self.parent.owner
		elif self.collection_type == 'series':
			return self.parent.parent.owner
	
	user = property(get_user)

	def get_absolute_url(self):
		
		if self.collection_type == 'library':
			return ('library_detail', [self.slug])
		elif self.collection_type == 'bookshelf':
			return ('bookshelf_detail', [self.parent.slug, self.slug])
		else:
			return None
	
	get_absolute_url = permalink(get_absolute_url)
	
	def __unicode__(self):
		"""
		Return a pretty formatted name
		"""
		return self.name
	
	def save(self, *args, **kwargs):
		'''
		Validation assertions ensures:
		A Library must: have an owner but no parent; not have that same name as another library from the same owner
		A Bookshelf must: not have an owner but must have a Library for a parent; not have the same name as a sibling bookshelf
		A Series must: not have an owner but must have a Bookshelf for a parent; not have the same name as a sibling series
		'''
		
		#assert re.match('^[a-zA-Z0-9\ \-\_]*$', self.name), 'The collection name can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
		
		self.slug = slugify(self.name)
		
		if self.collection_type == 'library':
			assert self.parent is None and self.owner is not None, 'A Library can not have a parent, and must have an owner'
			
		elif self.collection_type == 'bookshelf':
			assert self.parent.collection_type == 'library' and self.owner is None, 'A Bookshelf must have a parent of type "library", and must not have an owner'
			
		elif self.collection_type == 'series':
			assert self.parent.collection_type == 'bookshelf' and self.owner is None, 'A Series must have a parent of type "bookshelf", and must not have an owner'
			
		else:
			raise AssertionError, 'A Collection must be of type "library", "bookshelf" or "series"'
		
		
		# The uniqueness constraints a collection must abide by
		constraint = {'collection_type': self.collection_type, 'owner': self.owner, 'parent': self.parent, 'slug': self.slug}
		
		lock = threading.Lock()
		lock.acquire()
		
		try:
		
			# Gather any collections which match those values
			collections = list(Collection.objects.filter(Q(**constraint) & ~Q(pk=self.pk)))
			
			if len(collections) == 0:
				# If there are no matches
				
				# Save the current collection
				super(Collection, self).save(*args, **kwargs)
				
			else:
				# Otherwise you cannot add the collection in its current state
				raise ValidationError('There already exists a collection of that collection type "parent or owner" and slug')
		
		finally:
			lock.release()
	
	def get_owner(self):
		"""
		Get the owner (User) of this collection
		"""
		
		if self.collection_type == 'library':
			return self.owner
		elif self.collection_type == 'bookshelf':
			return self.parent.owner
		elif self.collection_type == 'series':
			return self.parent.parent.owner
		else:
			return None