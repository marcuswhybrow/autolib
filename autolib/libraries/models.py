# Allows classes to extend the models amd forms classes.
from django.db import models
from django.db.models import permalink
from django import forms

# Allows referencing the user.
from django.contrib.auth.models import User
from django.utils.http import urlquote_plus
import managers
import re

#########################
### Collections Model ###
#########################

COLLECTION_TYPE_CHOICES = (
	('library', 'Library'),
	('bookshelf', 'Book Shelf'),
	('series', 'Series'),
)

from base.models import Syncable

class Collection(Syncable):
	class Meta:
		unique_together = (('collection_type', 'owner', 'name'),('collection_type', 'parent', 'name'))
	
	name = models.CharField(max_length=200)
	collection_type = models.CharField(max_length=20, choices=COLLECTION_TYPE_CHOICES)
	description = models.CharField(max_length=1024, null=True, blank=True)
	parent = models.ForeignKey('self', related_name="children", null=True, blank=True)
	owner = models.ForeignKey(User, related_name="libraries", null=True, blank=True)
	
	objects = models.Manager()
	libraries = managers.LibraryManager()
	bookshelves = managers.BookshelfManager()
	series = managers.SeriesManager()
	

	def get_absolute_url(self):
		if self.collection_type == 'library':
			return ('library_detail', [self.owner.username, self.get_slug()])
						
		elif self.collection_type == 'bookshelf':
			return ('bookshelf_detail', [self.parent.owner.username, self.parent.get_slug(), self.get_slug()])
		
		return None
	
	get_absolute_url = permalink(get_absolute_url)
	
	def __unicode__(self):
		'''
		Return a pretty formatted name depending on Collection type.
		'''
		
		if self.collection_type == 'library':
			return '[%s - %s] %s' % (self.get_collection_type_display(), self.owner, self.name)
		else:
			return '[%s] %s' % (self.get_collection_type_display(), self.name)
	
	def get_slug(self):
		return urlquote_plus(self.name)
	
	def save(self, *args, **kwargs):
		'''
		Validation assertions ensures:
		A Library must: have an owner but no parent; not have that same name as another library from the same owner
		A Bookshelf must: not have an owner but must have a Library for a parent; not have the same name as a sibling bookshelf
		A Series must: not have an owner but must have a Bookshelf for a parent; not have the same name as a sibling series
		'''
		
		assert re.match('^[a-zA-Z0-9\ \-\_]*$', self.name), 'The collection name can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
		
		if self.collection_type == 'library':
			assert self.parent is None and self.owner is not None, 'A Library can not have a parent, and must have an owner'
			
		elif self.collection_type == 'bookshelf':
			assert self.parent.collection_type == 'library' and self.owner is None, 'A Bookshelf must have a parent of type "library", and must not have an owner'
			
		elif self.collection_type == 'series':
			assert self.parent.collection_type == 'bookshelf' and self.owner is None, 'A Series must have a parent of type "bookshelf", and must not have an owner'
			
		else:
			raise AssertionError, 'A Collection must be of type "library", "bookshelf" or "series"'
		
		super(self.__class__, self).save(*args, **kwargs)
	
	def get_owner(self):
		if self.collection_type == 'library':
			return self.owner
		elif self.collection_type == 'bookshelf':
			return self.parent.owner
		elif self.collection_type == 'series':
			return self.parent.parent.owner
			
		return None