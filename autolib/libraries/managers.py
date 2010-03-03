from django.db import models

from base.models import UUIDSyncableManager

class LibraryManager(UUIDSyncableManager):
	def get_query_set(self):
		return super(LibraryManager, self).get_query_set().filter(collection_type='library')

class BookshelfManager(UUIDSyncableManager):
	def get_query_set(self):
		return super(BookshelfManager, self).get_query_set().filter(collection_type='bookshelf')

class SeriesManager(UUIDSyncableManager):
	def get_query_set(self):
		return super(SeriesManager, self).get_query_set().filter(collection_type='series')