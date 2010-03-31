##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from django.db import models
import inspect

class UUIDSyncableManager(models.Manager):
	
	use_for_related_fields = False
	
	def get_query_set(self):
		return super(UUIDSyncableManager, self).get_query_set().filter(is_deleted=False)

class UUIDSyncableDeletedManager(models.Manager):
	
	use_for_related_fields = False
	
	def get_query_set(self):
		return super(UUIDSyncableDeletedManager, self).get_query_set().filter(is_deleted=True)