# api.views.insert

from django.db import IntegrityError, DatabaseError
from api.views import APIAuthView
from libraries.models import Collection
from books.models import BookProfile, Book
from django.db.models import Q

class SaveCollection(APIAuthView):
	def process(self, request):
		pk = request.POST.get('pk', None)
		name = request.POST.get('name', None)
		description = request.POST.get('description', None)
		parent_pk = request.POST.get('parent_pk', None)
		collection_type = request.POST.get('collection_type', None)
					
		if pk is not None:
			try:
				collection = Collection.objects.get(Q(pk=pk) & (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
				
				if name is not None: collection.name = name
				if description is not None: collection.description = description
				
				collection.save() # Errors caught by APIAuthView super class
				
			except Collection.DoesNotExist:
				self.data['meta']['error'] = 'A Collection with the pk ' + str(collection.pk) + ' does not exist for this User, and therefor cannot be updated'
				return
				
		else:
			if collection_type is not None and name is not None:
				kwargs = {}
				kwargs['collection_type'] = collection_type
				try:
					if collection_type == 'bookshelf' or collection_type == 'series':
						if parent_pk is not None:
							kwargs['parent'] = Collection.objects.get(Q(pk=parent_pk) & (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
						else:
							self.data['meta']['error'] = 'parent_pk was not found and is required when creating a Collection which is not a library'
							return
					
					if name is not None: kwargs['name'] = name
					if description is not None: kwargs['description'] = description
					if collection_type == 'library': kwargs['owner'] = self.user
					
					collection = Collection(**kwargs)
					collection.save() # Errors caught by APIAuthView super class
					
					print collection
					
				except Collection.DoesNotExist:
					self.data['meta']['error'] = 'Parent collection with pk ' + str(parent_pk) + ' does not exist for this User'
					return
			else:
				self.data['meta']['error'] = 'collection_type, parent_pk or name not found (all required) in the POST data'
				return
					
		
		self.data['collection'] = {
			'pk': collection.pk,
			'name': collection.name,
			'slug': collection.slug,
			'description': collection.description,
			'url': collection.get_absolute_url() if collection.collection_type != 'series' else None,
			'added': str(collection.added),
			'last_modified': str(collection.last_modified),
		}
		
		self.data['meta']['success'] = True

from books.utils import GoogleAdapter
from tagging.models import Tag
from django.template.defaultfilters import slugify

class SaveProfile(APIAuthView):
	def process(self, request):
		pk = request.POST.get('pk', None)
		collection_pk = request.POST.get('collection_pk', None)
		
		if pk is not None:
			try:
				profile = BookProfile.objects.get(Q(pk=pk) & (Q(collection__owner=self.user) | Q(collection__parent__owner=self.user) | Q(collection__parent__parent__owner=self.user)))
				collection = Collection.objects.get(Q(pk=collection_pk) & (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
				
				profile.collection = collection
				profile.save()
								
				self.data['profile'] = {
					'book_instance': profile.book_instance.pk,
					'collection': profile.collection.pk,
					'added': str(profile.added),
					'last_modified': str(profile.last_modified),
				}
				self.data['meta']['success'] = True
				return
				
			except BookProfile.DoesNotExist:
				self.data['meta']['error'] = "A BookProfile with pk " + pk + " was not found for this User"
				return
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "A Collection with pk " + pk + " was not found for this User"
				return
			
		else:
			isbn = request.POST.get('isbn', None)
			if isbn is not None:
				if collection_pk is not None:
					try:
						collection = Collection.objects.get(Q(pk=collection_pk) & (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
						try:
							if len(isbn) == 10:
								book = Book.objects.get(isbn10=isbn)
							elif len(isbn) == 13:
								book = Book.objects.get(isbn13=isbn)
							else:
								self.data['meta']['error'] = 'ISBN must be 10 or 13 characters in length'
								return
						except Book.DoesNotExist:
							details = GoogleAdapter(isbn)
							
							if details.get_details() is not None:
								book = Book(**details.get_details())
								print details.get_details()
								book.save()
							else:
								self.data['meta']['error'] = 'ISBN not found using Google Books'
								return
							
							for subject in details.get_subjects():
								Tag.objects.add_tag(book, slugify(subject))
							
						try:
							profile = BookProfile(book_instance=book, collection=collection)
							profile.save()
							self.data['profile'] = {
								'book_instance': profile.book_instance.pk,
								'collection': profile.collection.pk,
								'added': str(profile.added),
								'last_modified': str(profile.last_modified),
							}
							self.data['book'] = {
								'isbn10': book.isbn10,
								'isbn13': book.isbn13,
								'title': book.title,
								'description': book.description,
								'author': book.author,
								'publisher': book.publisher,
								'published': str(book.published),
								'pages': book.pages,
								'width': book.width,
								'height': book.height,
								'depth': book.depth,
								'format': book.format,
								'language': book.language,
								'added': str(profile.added),
								'last_modified': str(profile.last_modified),
							}
							self.data['meta']['success'] = True
							return
							
						except Book.DoesNotExist:
							self.data['meta']['error'] = "A Book with that pk was not found"
					
					except Collection.DoesNotExist:
						self.data['meta']['error'] = "A Collection with that pk does not exist for this user"
				else:
					self.data['meta']['error'] = "collection_pk was not found"
			else:
				self.data['meta']['error'] = "isbn was not found"

save_collection = SaveCollection()
save_profile = SaveProfile()