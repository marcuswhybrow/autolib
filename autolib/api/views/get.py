# api.views.get

from libraries.models import Collection
from volumes import utils
from volumes.models import BookProfile, Book
from api.views import APIView, APIAuthView

from django.db.models import Q

from django.core.urlresolvers import NoReverseMatch

class GetCollectionList(APIAuthView):
	def process(self, request):
		parent_pk = request.POST.get('parent_pk', None) or request.POST.get('pk', None)
		if parent_pk is not None:
			try:
				collection = Collection.objects.get(Q(pk=parent_pk)& (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
				self.data['collections'] = []
				
				for c in collection.children.all():
					
					try:
						url = c.get_absolute_url()
					except NoReverseMatch:
						url = None
					
					self.data['collections'].append({
						'pk': c.pk,
						'name': c.name,
						'parent': c.parent.pk if c.parent is not None else None,
						'slug': c.slug,
						'description': c.description,
						'url': url,
						'added': str(c.added),
						'last_modified': str(c.last_modified),
					})
				self.data['meta']['success'] = True
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "Library not found with that pk, for that user"
		else:
			self.data['collections'] = []
			for c in self.user.libraries.all():
				
				try:
					url = c.get_absolute_url()
				except NoReverseMatch:
					url = None
				
				self.data['collections'].append({
					'pk': c.pk,
					'name': c.name,
					'parent': c.parent.pk if c.parent is not None else None,
					'slug': c.slug,
					'description': c.description,
					'url': c.get_absolute_url(),
					'added': str(c.added),
					'last_modified': str(c.last_modified),
				})
			self.data['meta']['success'] = True

class GetCollectionDetail(APIAuthView):
	
	def process(self, request):
		collection_pk = request.POST.get('collection_pk', None) or request.POST.get('pk', None)
		if collection_pk is not None:
			try:
				c = Collection.objects.get(Q(pk=collection_pk)& (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user))) # TODO use Q again
				
				try:
					url = c.get_absolute_url()
				except NoReverseMatch:
					url = None
				
				self.data['collection'] = {
					'pk': c.pk,
					'name': c.name,
					'parent': c.parent.pk if c.parent is not None else None,
					'description': c.description,
					'url': url,
					'slug': c.slug,
					'added': str(c.added),
					'last_modified': str(c.last_modified),
				}
				self.data['meta']['success'] = True
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "Library not found with that pk, for that user"
		else:
			self.data['meta']['error'] = "collection_pk not found"

class GetBookProfileList(APIAuthView):
	
	def process(self, request):
		collection_id = request.POST.get('collection_pk', None) or request.POST.get('pk', None)
		if collection_id is not None:
			try:
				c = Collection.objects.get(Q(pk=collection_id)& (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
				
				self.data['profiles'] = []
				for p in c.books.all():
					
					try:
						url = p.get_absolute_url()
					except NoReverseMatch:
						url = None
					
					self.data['profiles'].append({
						'collection': p.collection.pk,
						'book_instance': p.book_instance.pk,
						'added': str(p.added),
						'last_modified': str(p.last_modified),
						'url': url,
					})
				self.data['meta']['success'] = True
						
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "Collection with that primary key does not exist, for this user"
		
		else:
			self.data['meta']['error'] = "collection_pk not found"

class GetBookProfileDetail(APIAuthView):
	
	def process(self, request):
		profile_pk = request.POST.get('profile_pk', None) or request.POST.get('pk', None)
		if profile_pk is not None:
			try:
				p = BookProfile.objects.get(Q(pk=profile_pk)& (Q(collection__owner=self.user) | Q(collection__parent__owner=self.user) | Q(collection__parent__parent__owner=self.user))) # TODO use Q again
				
				try:
					url = p.get_absolute_url()
				except NoReverseMatch:
					url = None
				
				self.data['profile'] = {
					'pk': p.book_instance.pk,
					'isbn': p.book_instance.isbn,
					'title': p.book_instance.title,
					'author': p.book_instance.author,
					'published': p.book_instance.published,
					'publisher': p.book_instance.publisher,
					'description': p.book_instance.description,
					'collection': p.collection.pk,
					'added': str(p.added),
					'last_modified': str(p.last_modified),
					'url': url,
				}
				self.data['meta']['success'] = True
						
			except BookProfile.DoesNotExist:
				self.data['meta']['error'] = "BookProfile with that primary key does not exist, for this user"
		
		else:
			self.data['meta']['error'] = "profile_pk not found"

class GetBookDetail(APIView):
	
	def process(self, request):
		"""
		Gets information about a book by its ISBN number or UUID pk from the local database,
		Uses google books to update the database if ISBN is used.
		"""
		
		# The ISBN number of the book
		isbn = request.GET.get('isbn', None)
		
		if isbn is not None:
			# If the ISBN number was provided
				
			book = None
			
			try:
				# Try to find the book locally
				if len(isbn) == 10:
					book = Book.objects.get(isbn10=isbn)
				elif len(isbn) == 13:
					book = Book.objects.get(isbn13=isbn)
				else:
					self.data['meta']['error'] = 'ISBN must be 10 or 13 characters in length'
					return
				
			except Book.DoesNotExist:
				# If not found locally try and get the book details from Google
				bookDetails = utils.get_book_detail(isbn)
				
				if bookDetails is not None:
					# If book details were found
					# Convert the details into a database object
					book = bookDetails.convert_to_book()
					
					# TODO Get Django to queue up the updating of this books Editions
					utils.UpdateEditions(book).start()
					
				else:
					self.data['meta']['error'] = 'Details for the book with the ISBN ' + isbn + ' not found'
					return
			
		else:
			# Otherwise get look for the a UUID pk of the Book
			book_pk = request.GET.get('pk', None)
			
			if book_pk is not None:
				try:
					# Try and get the Book based on that pk
					book = Book.objects.get(pk=book_pk)
					
				except Book.DoesNotExist:
					# If it doesn't exist
					
					self.data['meta']['error'] = 'Details for the book with the pk' + book_pk + ' not found'
					return
			else:
				# If the book_pk was not supplied
				self.data['meta']['error'] = "Neither isbn or pk was found in the GET data"
				return
		
		if book is not None:
			
			try:
				url = book.get_absolute_url()
			except NoReverseMatch:
				url = None
			
			self.data['book'] = {
				'pk': book.pk,
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
				'added': str(book.added),
				'last_modified': str(book.last_modified),
				'edition_group': book.edition_group.pk,
				'url': url,
				'thumbnail_large': book.thumbnail_large,
				'thumbnail_small': book.thumbnail_small,
			}
			self.data['meta']['success'] = True

get_collection_list = GetCollectionList()
get_collection_detail = GetCollectionDetail()
get_profile_list = GetBookProfileList()
get_profile_detail = GetBookProfileDetail()
get_book_detail = GetBookDetail()