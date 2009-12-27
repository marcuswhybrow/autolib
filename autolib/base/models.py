from django.db import models

# Create your models here.

class Config(models.Model):
	'''
	System-wide configuration, key value pairs (with slug) which allow important 
	values such as naming schemes to be altered later on.
	'''
	
	key = models.CharField(max_length=200, primary_key=True)
	value = models.CharField(max_length=200)
	slug = models.SlugField()
	
	def __unicode__(self):
		return '%s : %s' % (self.key, self.value)