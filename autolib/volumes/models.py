from django.db import models
from django.db.models import permalink
from.django import forms

from libraries.models import Collection
from base.models import Config

from django.utils.http import urlquote_plus
from django.template.defaultfilters import slugify

from django.core.exceptions import ValidationError
from django.db.models import Q

import re

##################
### Book Model ###
##################

from base.models import UUIDSyncable
from tagging.fields import TagField
from tagging.models import Tag
import tagging

class BookEditionGroup(UUIDSyncable):
	
	def get_owner(self):
		return None
	
	def __unicode__(self):
		try:
			return self.editions.all()[0].title
		except IndexError:
			return 'EMPTY'

class Book(UUIDSyncable):
	
	thumbnail_large = models.URLField(null=True)
	thumbnail_small = models.URLField(null=True)
	
	isbn10 = models.CharField(db_index=True, unique=True, editable=False, max_length=10)
	isbn13 = models.CharField(db_index=True, unique=True, editable=False, max_length=13)
	title = models.CharField(max_length=100)
	description = models.TextField(null=True)
	author = models.CharField(max_length=100, null=True)
	publisher = models.CharField(max_length=100, null=True)
	published = models.DateTimeField(null=True)
	pages = models.IntegerField(null=True)
	width = models.FloatField(null=True)
	height = models.FloatField(null=True)
	depth = models.FloatField(null=True)
	format = models.CharField(max_length=100, null=True)
	language = models.CharField(max_length=5, null=True)
	
	edition_group = models.ForeignKey(BookEditionGroup, related_name='editions', editable=False)
	
	def get_tags(self):
		return Tag.objects.get_for_object(self)
	
	def set_tags(self, tag_list):
		Tag.objects.update_tags(self, tag_list)
	
	tags = property(get_tags, set_tags)
	
	class Meta:
		ordering = ('-published', )
		get_latest_by = 'published'

	
	def get_tags(self):
		return Tag.objects.get_for_object(self)
	
	def __unicode__(self):
		return self.title
		
	def get_isbn(self):
		if self.isbn10:
			return self.isbn10
		elif self.isbn13:
			return self.isbn13
		
		return None
	
	isbn = property(get_isbn)
	
	@permalink
	def get_absolute_url(self):
		return ('volumes.views.book_detail', [self.isbn])
	
	def get_owner(self):
		return None

#tagging.register(Book)

class BookProfile(UUIDSyncable):
	book_instance = models.ForeignKey(Book, related_name='instances')
	collection = models.ForeignKey(Collection, related_name='books')
	slug = models.CharField(max_length=100, editable=False)
		
	def get_tags(self):
		return Tag.objects.get_for_object(self) 
	
	def __unicode__(self):
		return self.book_instance.title
	
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
	
	@property
	def isbn(self):
		return self.book_instance.isbn
	
	@property
	def isbn10(self):
		return self.book_instance.isbn10
	
	@property
	def isbn13(self):
		return self.book_instance.isbn13
	
	@property
	def title(self):
		return self.book_instance.title
	
	@property
	def description(self):
		return self.book_instance.description
	
	@property
	def author(self):
		return self.book_instance.author
		
	@property
	def publisher(self):
		return self.book_instance.publisher
	
	@property
	def published(self):
		return self.book_instance.published
	
	@property
	def pages(self):
		return self.book_instance.pages
	
	@property
	def width(self):
		return self.book_instance.width
	
	@property
	def height(self):
		return self.book_instance.height
	
	@property
	def depth(self):
		return self.book_instance.depth
	
	@property
	def format(self):
		return self.book_instance.format
	
	@property
	def language(self):
		return self.book_instance.language
	
	@property
	def edition_group(self):
		return self.book_instance.edition_group
	
	@property
	def thumbnail_large(self):
		return self.book_instance.thumbnail_large
	
	@property
	def thumbnail_small(self):
		return self.book_instance.thumbnail_small
	
	def get_owner(self):
		if self.collection.collection_type == 'library':
			return self.collection.owner
		elif self.collection.collection_type == 'bookshelf':
			return self.collection.parent.owner
		elif self.collection.collection_type == 'series':
			return self.collection.parent.parent.owner
		else:
			return None
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		
		uniqueConstraint = {'book_instance': self.book_instance, 'collection': self.collection}
		
		profiles = BookProfile.objects.filter(Q(**uniqueConstraint) & ~Q(pk=self.pk))
		
		if len(profiles) == 0:
			super(BookProfile, self).save(*args, **kwargs)
		else:
			raise ValidationError('A Book Profile for that book instance in that collection already exists')

#tagging.register(BookProfile)

class Note(UUIDSyncable):
	
	profile = models.ForeignKey(BookProfile, related_name='notes')
	note = models.TextField()
	
	def __unicode__(self):
		return 'Note for %s' % (self.profile.title)
	
	def get_owner(self):
		return self.profile.get_owner()
		
#############
### Forms ###
#############

class BookForm(forms.ModelForm):
	
	class Meta:
		model = Book

class BookProfileForm(forms.ModelForm):
	
	class Meta:
		model = BookProfile
	