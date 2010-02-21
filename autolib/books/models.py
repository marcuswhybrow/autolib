from django.db import models
from django.db.models import permalink
from.django import forms

from libraries.models import Collection
from base.models import Config

from django.utils.http import urlquote_plus
from django.template.defaultfilters import slugify

import re

##################
### Book Model ###
##################

from base.models import UUIDSyncable
from tagging.fields import TagField
from tagging.models import Tag
import tagging

class Book(UUIDSyncable):
	
	isbn10 = models.CharField(db_index=True, unique=True, editable=False, max_length=10)
	isbn13 = models.CharField(db_index=True, unique=True, editable=False, max_length=13)
	title = models.CharField(max_length=200)
	description = models.TextField(null=True)
	author = models.CharField(max_length=200, null=True)
	publisher = models.CharField(max_length=200, null=True)
	published = models.DateTimeField(null=True)
	pages = models.IntegerField(null=True)
	width = models.FloatField(null=True)
	height = models.FloatField(null=True)
	depth = models.FloatField(null=True)
	format = models.CharField(max_length=200, null=True)
	language = models.CharField(max_length=5, null=True)
	
# 	tags = TagField()
# 	
# 	def get_tags(self):
# 		return Tag.objects.get_for_object(self) 

	def __unicode__(self):
		return '[Book] %s' % self.isbn
		
	def get_isbn(self):
		if self.isbn10:
			return self.isbn10
		elif self.isbn13:
			return self.isbn13
		
		return None
	
	isbn = property(get_isbn)
	
# 	def save(self, *args, **kwargs):
# 		assert re.match('^[a-zA-Z0-9\ \-\_]*$', self.title), 'A title can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
# 		super(self.__class__, self).save(*args, **kwargs)
	
	@permalink
	def get_absolute_url(self):
		return ('books.views.book_detail', [self.isbn])
	
	def get_owner(self):
		return None

tagging.register(Book)

class BookProfile(UUIDSyncable):
	book_instance = models.ForeignKey(Book, related_name='instances')
	collection = models.ForeignKey(Collection, related_name='books')
	slug = models.CharField(max_length=200, editable=False)
	
# 	tags = TagField()
# 	
# 	def get_tags(self):
# 		return Tag.objects.get_for_object(self) 
	
	class Meta:
		unique_together = ('book_instance', 'collection')
	
	def __unicode__(self):
		return '[BookProfile] %s' % self.book_instance.isbn
	
	@permalink
	def get_absolute_url(self):
		if self.collection.collection_type == 'library':
			bookshelf = Config.objects.get(key='unsorted_bin').slug
			library = self.collection.slug
		elif self.collection.collection_type == 'bookshelf':
			bookshelf = self.collection.slug
			library = self.collection.parent.slug
		elif self.collection.collection_type == 'series':
			bookshelf = self.collection.parent.slug
			library = self.collection.parent.parent.slug
		
		return ('profile_detail', [library, bookshelf, self.isbn, self.slug])
	
	def get_isbn(self):
		return self.book_instance.isbn
	
	def get_title(self):
		return self.book_instance.title
	
	def get_description(self):
		return self.book_instance.description
	
	def get_author(self):
		return self.book_instance.author
		
	def get_publisher(self):
		return self.book_instance.publisher
	
	def get_published(self):
		return self.book_instance.published
	
	def get_pages(self):
		return self.book_instance.pages
	
	def get_width(self):
		return self.book_instance.width
	
	def get_height(self):
		return self.book_instance.height
	
	def get_depth(self):
		return self.book_instance.depth
	
	def get_format(self):
		return self.book_instance.format
	
	def get_language(self):
		return self.book_instance.language
	
	def get_owner(self):
		if self.collection.collection_type == 'library':
			return self.collection.owner
		elif self.collection.collection_type == 'bookshelf':
			return self.collection.parent.owner
		elif self.collection.collection_type == 'series':
			return self.collection.parent.parent.owner
		else:
			return None
	
	isbn = property(get_isbn)
	title = property(get_title)
	description = property(get_description)
	author = property(get_author)
	publisher = property(get_publisher)
	published = property(get_published)
	user = property(get_owner)
	pages = property(get_pages)
	width = property(get_width)
	height = property(get_height)
	depth = property(get_depth)
	format = property(get_format)
	language = property(get_language)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(BookProfile, self).save(*args, **kwargs)

tagging.register(BookProfile)
		
#############
### Forms ###
#############

class BookForm(forms.ModelForm):
	
	class Meta:
		model = Book

class BookProfileForm(forms.ModelForm):
	
	class Meta:
		model = BookProfile
	