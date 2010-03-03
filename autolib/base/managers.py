from django.db import models

class UUIDSyncableManager(models.Manager):
	
	def get_query_set(self):
		return super(UUIDSyncableManager, self).get_query_set().filter(isDeleted=False)

class UUIDSyncableDeletedManager(models.Manager):
	
	def get_query_set(self):
		return super(UUIDSyncableDeletedManager, self).get_query_set().filter(isDeleted=True)