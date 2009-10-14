# Allows classes to extend the models amd forms classes.
from django.db import models
from.django import forms

# Allows referencing the user.
from django.contrib.auth.models import User

# A Library can contain of books, and is ownded by a single person.
class Library(models.Model):
	name = models.CharField(max_length=200)
	owner = models.ForeignKey(User, related_name="libraries")
	
	def __unicode__(self):
		return self.name

# A Book is contained with a single library 
class Book(models.Model):
	isbn = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=200, null=True)
	author = models.CharField(max_length=200, null=True)
	library = models.ForeignKey(Library, related_name="books") 

	def __unicode__(self):
		return self.title

# Forms
class BookForm(forms.Form):
	isbn = forms.IntegerField()
	title = forms.CharField(max_length=200)
	author = forms.CharField(max_length=200)
	library = forms.ModelChoiceField(queryset=Library.objects.all(), empty_label="-- Pick a Library --")
