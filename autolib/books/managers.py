from django.db import models

class LibraryManager(models.Manager):
	def get_query_set(self):
		return super(self.__class__, self).get_query_set().filter(type='library')

class BookshelfManager(models.Manager):
	def get_query_set(self):
		return super(self.__class__, self).get_query_set().filter(type='bookshelf')

class SeriesManager(models.Manager):
	def get_query_set(self):
		return super(self.__class__, self).get_query_set().filter(type='series')