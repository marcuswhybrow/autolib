from django import forms
from libraries.models import Collection

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
	
# 	def clean(self):
# 		collection_type = self.cleaned_data['collection_type']
# 		owner = self.cleaned_data.get('owner', None)
# 		parent = self.cleaned_data.get('parent', None)
# 		
# 		if collection_type == 'library' and owner is not None and parent is None \
# 		or collection_type == 'bookshelf' and owner is None and parent is not None \
# 		or collection_type == 'series' and owner is None and parent is not None:
# 			return self.cleaned_data
# 		else:
# 			raise forms.ValidationError(u'A Library must have an owner (but no parent), a Bookshelf and Series must have a parent (but no owner).')
		
	
# 	def save(self, args*, kwargs**):
# 		if not self.is_valid():
# 			raise ValueError("Cannot save from an invalid form")
# 		name = self.cleaned_data['name']
# 		return Collection.objects.create(name=name, collection_type=self.collection_type, owner=self.owner, parent=self.parent)
				
class CreateCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner']

class UpdateCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'description', 'collection_type', 'parent']

class EditCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'collection_type', 'parent']