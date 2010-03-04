from django.db import models

class UUIDSyncableManager(models.Manager):
	
	use_for_related_fields = True
	
	def get_query_set(self):
		return super(UUIDSyncableManager, self).get_query_set().filter(is_deleted=False)

class UUIDSyncableDeletedManager(models.Manager):
	
	use_for_related_fields = True
	
	def get_query_set(self):
		return super(UUIDSyncableDeletedManager, self).get_query_set().filter(is_deleted=True)