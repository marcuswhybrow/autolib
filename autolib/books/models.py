from django.db import models
from django.db.models import permalink
from.django import forms

from libraries.models import Collection
from base.models import Config

from django.utils.http import urlquote_plus

import re

##################
### Book Model ###
##################

class Book(models.Model):
	isbn = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=200)
	description = models.TextField()
	author = models.CharField(max_length=200)
	publisher = models.CharField(max_length=200)
	published = models.DateField()

	def __unicode__(self):
		return '[Book] %s' % self.isbn
	
# 	def save(self, *args, **kwargs):
# 		assert re.match('^[a-zA-Z0-9\ \-\_]*$', self.title), 'A title can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
# 		super(self.__class__, self).save(*args, **kwargs)
	
	@permalink
	def get_absolute_url(self):
		return ('books.views.book_detail', [self.isbn])

class BookProfile(models.Model):
	book_instance = models.ForeignKey(Book, related_name='instances')
	collection = models.ForeignKey(Collection, related_name='books')
	
	def __unicode__(self):
		return '[BookProfile] %s' % self.book_instance.isbn
	
	def get_slug(self):
		return re.sub('\ ', '-', re.sub('[^a-zA-Z0-9\ \-\_]', '', self.book_instance.title))
	
	@permalink
	def get_absolute_url(self):
		if self.collection.collection_type == 'library':
			bookshelf = Config.objects.get(key='unsorted_bin').slug
			library = self.collection.get_slug()
			username = self.collection.owner.username
		elif self.collection.collection_type == 'bookshelf':
			bookshelf = self.collection.get_slug()
			library = self.collection.parent.get_slug()
			username = self.collection.parent.owner.username
		elif self.collection.collection_type == 'series':
			bookshelf = self.collection.parent.get_slug()
			library = self.collection.parent.parent.get_slug()
			username = self.collection.parent.parent.owner.username
		
		return ('users.views.book_detail', [username, library, bookshelf, self.book_instance.isbn, self.get_slug()])
	
	def isbn(self):
		return self.book_instance.isbn
	
	def title(self):
		return self.book_instance.title
	
	def description(self):
		return self.book_instance.description
	
	def author(self):
		return self.book_instance.author
		
	def publisher(self):
		return self.book_instance.publisher
	
	def published(self):
		return self.book_instance.published
		
#############
### Forms ###
#############

class BookForm(forms.ModelForm):
	
	class Meta:
		model = Book
	