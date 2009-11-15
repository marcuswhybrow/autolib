# Allows classes to extend the models amd forms classes.
from django.db import models
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
	name = models.CharField(max_length=200)
	type = models.CharField(max_length=20, choices=COLLECTION_TYPE_CHOICES)
	description = models.CharField(max_length=1024, null=True, blank=True)
	parent = models.ForeignKey('self', related_name="children", null=True, blank=True)
	owner = models.ForeignKey(User, related_name="libraries", null=True, blank=True)
	
	objects = models.Manager()
	libraries = managers.LibraryManager()
	bookshelves = managers.BookshelfManager()
	series = managers.SeriesManager()
	
	def get_absolute_url(self):
		if self.type == 'library':
			return '/libraries/%s/' % quote_plus(self.name)
			
		elif self.type == 'bookshelf':
			return '/libraries/%s/%s/' % (quote_plus(self.parent.name), quote_plus(self.name))
	
	def __unicode__(self):
		'''
		Return a pretty formatted name depending on Collection type.
		'''
		
		if self.type == 'library':
			return '[%s - %s] %s' % (self.get_type_display(), self.owner, self.name)
		else:
			return '[%s] %s' % (self.get_type_display(), self.name)
	
	def save(self, *args, **kwargs):
		'''
		Validation assertions ensures:
		A Library must: have an owner but no parent; not have that same name as another library from the same owner
		A Bookshelf must: not have an owner but must have a Library for a parent; not have the same name as a sibling bookshelf
		A Series must: not have an owner but must have a Bookshelf for a parent; not have the same name as a sibling series
		'''
		
		if self.type == 'library':
			assert self.parent is None and self.owner is not None, 'A Library can not have a parent, and must have an owner'
			for library in self.owner.libraries.all():
				assert self.name != library.name
			
		elif self.type == 'bookshelf':
			assert self.parent.type == 'library' and self.owner is None, 'A Bookshelf must have a parent of type "library", and must not have an owner'
			for bookshelf in self.parent.children.all():
				assert self.name != bookshelf.name
			
		elif self.type == 'series':
			assert self.parent.type == 'bookshelf' and self.owner is None, 'A Series must have a parent of type "bookshelf", and must not have an owner'
			for series in self.parent.children.all():
				assert self.name != series.name
			
		else:
			raise AssertionError, 'A Collection must be of type "library", "bookshelf" or "series"'
		
		super(self.__class__, self).save(*args, **kwargs)

##################
### Book Model ###
##################

class Book(models.Model):
	isbn = models.IntegerField()
	collection = models.ForeignKey(Collection, related_name="books")

	def __unicode__(self):
		return '[Book] %s' % self.isbn

#############
### Forms ###
#############

class BookForm(forms.Form):
	isbn = forms.IntegerField()
	
class CollectionForm(forms.ModelForm):
	class Meta:
		model = Collection
		exclude = ['owner']
		
class NewCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'description', 'type', 'parent']

class EditCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'type', 'parent']

'''
class LibraryForm(CollectionForm):
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		del self.fields['parent']

class BookshelfForm(CollectionForm):
	def __init__(self):
		super(self.__class__, self).__init__(*args, **kwargs)
		
		#parent = some library, owner = null

class SeriesForm(CollectionForm):
	def __init__(self):
		pass
		#parent = some bookshelf, owner = null

'''