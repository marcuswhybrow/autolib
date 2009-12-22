from django.db import models
from django.db.models import permalink
from.django import forms

from libraries.models import Collection

##################
### Book Model ###
##################

class Book(models.Model):
	isbn = models.IntegerField()
	collection = models.ForeignKey(Collection, related_name="books")

	def __unicode__(self):
		return '[Book] %s' % self.isbn
	
	def get_absolute_url(self):
		return ('book_detail', [self.isbn])
	
	get_absolute_url = permalink(get_absolute_url)

#############
### Forms ###
#############

class BookForm(forms.Form):
	isbn = forms.IntegerField()