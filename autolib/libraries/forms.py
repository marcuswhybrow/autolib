from django import forms
from libraries.models import Collection
from django.contrib.auth.models import User

import re

class CollectionForm(forms.ModelForm):
	collection_type = None
	owner = None
	parent = None
	
	class Meta:
		model = Collection
	
	def clean_name(self):
		
		name = self.cleaned_data['name']
		
		try:
			Collection.objects.get(name=name, collection_type=self.collection_type, owner=self.owner)
		except Collection.DoesNotExist:
			if not re.match('^[a-zA-Z0-9\ \-\_]*$', name):
				raise forms.ValidationError(u'The collection name can only contain the characters: a-z, A-Z, 0-9, spaces, underscores and dashes.')
			else:
				return name
		raise forms.ValidationError(u'You already have a Library of that name.')
				
class CreateCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner']

class UpdateCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'description', 'collection_type', 'parent']

class EditCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'collection_type', 'parent']


class UserChangeForm(forms.ModelForm):
	
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']