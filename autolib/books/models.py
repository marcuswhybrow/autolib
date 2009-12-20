from django.db import models
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

#############
### Forms ###
#############

class BookForm(forms.Form):
	isbn = forms.IntegerField()