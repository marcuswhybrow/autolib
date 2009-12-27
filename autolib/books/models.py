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
	isbn = models.IntegerField()
	collection = models.ForeignKey(Collection, related_name="books")
	title = models.CharField(max_length=200)

	def __unicode__(self):
		return '[Book] %s' % self.isbn
	
	def get_absolute_url(self):
		if self.collection.collection_type == 'library':
			bookshelf = Config.objects.get(key='unsorted_bin').slug
			library = self.collection.get_slug()
			username = self.collection.owner.username
		elif collection.collection_type == 'bookshelf':
			bookshelf = self.collection.get_slug()
			library = self.collection.parent.get_slug()
			username = self.collection.parent.owner.username
		elif collection.collection_type == 'series':
			bookshelf = self.collection.parent.get_slug()
			library = self.collection.parent.parent.get_slug()
			username = self.collection.parent.parent.owner.username
		
		return ('libraries.views.book_detail', [username, library, bookshelf, self.isbn, self.title])
	
	get_absolute_url = permalink(get_absolute_url)
	
	def get_slug(self):
		return urlquote_plus(self.title)
	
	def save(self, *args, **kwargs):
		assert re.match('^[a-zA-Z0-9\ \-\_]*$', self.title), 'A title can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.'
		super(self.__class__, self).save(*args, **kwargs)

#############
### Forms ###
#############

class BookForm(forms.Form):
	isbn = forms.IntegerField()