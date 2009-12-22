# Allows classes to extend the models amd forms classes.
from django.db import models
from django.db.models import permalink
from.django import forms

# Allows referencing the user.
from django.contrib.auth.models import User

import managers

from urllib import quote_plus

#########################
### Collections Model ###
#########################

COLLECTION_TYPE_CHOICES = (
	('library', 'Library'),
	('bookshelf', 'Book Shelf'),
	('series', 'Series'),
)

class Collection(models.Model):
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
			return ('library_detail', [quote_plus(self.name)])
						
		elif self.collection_type == 'bookshelf':
			return ('bookshelf_detail', [quote_plus(self.parent.name), quote_plus(self.name)] )
	
	get_absolute_url = permalink(get_absolute_url)
	
	def __unicode__(self):
		'''
		Return a pretty formatted name depending on Collection type.
		'''
		
		if self.collection_type == 'library':
			return '[%s - %s] %s' % (self.get_collection_type_display(), self.owner, self.name)
		else:
			return '[%s] %s' % (self.get_collection_type_display(), self.name)
	
	def save(self, *args, **kwargs):
		'''
		Validation assertions ensures:
		A Library must: have an owner but no parent; not have that same name as another library from the same owner
		A Bookshelf must: not have an owner but must have a Library for a parent; not have the same name as a sibling bookshelf
		A Series must: not have an owner but must have a Bookshelf for a parent; not have the same name as a sibling series
		'''
		
		if self.collection_type == 'library':
			assert self.parent is None and self.owner is not None, 'A Library can not have a parent, and must have an owner'
			
		elif self.collection_type == 'bookshelf':
			assert self.parent.collection_type == 'library' and self.owner is None, 'A Bookshelf must have a parent of type "library", and must not have an owner'
			
		elif self.collection_type == 'series':
			assert self.parent.collection_type == 'bookshelf' and self.owner is None, 'A Series must have a parent of type "bookshelf", and must not have an owner'
			
		else:
			raise AssertionError, 'A Collection must be of type "library", "bookshelf" or "series"'
		
		super(self.__class__, self).save(*args, **kwargs)

#############
### Forms ###
#############
	
class CollectionForm(forms.ModelForm):
	collection_type = None
	user = None
	parent = None
	
	class Meta:
		model = Collection
		exclude = ['owner']
		
	def __init__(self, *args, **kwargs):
		self.collection_type = kwargs.pop('collection_type')
		if self.collection_type == 'library':
			self.user = kwargs.pop('user', None)
		elif self.collection_type == 'bookshelf' or self.collection_type == 'series':
			self.parent = kwargs.pop('parent', None)
		else:
			raise AssertionError, 'collection_type must be "library", "bookshelf" or "series"'
		super(CollectionForm, self).__init__(*args, **kwargs)
	
	def clean_name(self):
		try:
			Collection.objects.get(name=self.cleaned_data['name'], collection_type=self.collection_type, owner=self.user)
		except Collection.DoesNotExist:
			return self.cleaned_data['name']
		raise forms.ValidationError(u'You already have a Library of that name.')
	
	def save(self):
		if not self.is_valid():
			raise ValueError("Cannot save from an invalid form")
		return Collection.objects.create(name=self.cleaned_data['name'], collection_type=self.collection_type, owner=self.user, parent=self.parent)
				
class CreateCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'description', 'collection_type', 'parent']

class EditCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'collection_type', 'parent']