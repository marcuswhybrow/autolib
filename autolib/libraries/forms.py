from django import forms
from libraries.models import Collection

class CollectionForm(forms.ModelForm):
	collection_type = None
	user = None
	parent = None
	
	class Meta:
		model = Collection
		exclude = ['owner']
		
	def __init__(self, *args, **kwargs):
		self.collection_type = kwargs.pop('collection_type')
		if self.collection_type == 'library':
			self.user = kwargs.pop('user', None)
		elif self.collection_type == 'bookshelf' or self.collection_type == 'series':
			self.parent = kwargs.pop('parent', None)
		else:
			raise AssertionError, 'collection_type must be "library", "bookshelf" or "series"'
		super(CollectionForm, self).__init__(*args, **kwargs)
	
	def clean_name(self):
		try:
			Collection.objects.get(name=self.cleaned_data['name'], collection_type=self.collection_type, owner=self.user)
		except Collection.DoesNotExist:
			return self.cleaned_data['name']
		raise forms.ValidationError(u'You already have a Library of that name.')
	
	def save(self):
		if not self.is_valid():
			raise ValueError("Cannot save from an invalid form")
		return Collection.objects.create(name=self.cleaned_data['name'], collection_type=self.collection_type, owner=self.user, parent=self.parent)
				
class CreateCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'description', 'collection_type', 'parent']

class EditCollectionForm(CollectionForm):
	class Meta(CollectionForm.Meta):
		exclude = ['owner', 'collection_type', 'parent']