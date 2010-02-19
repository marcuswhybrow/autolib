# api.views.get

from libraries.models import Collection
from books.models import BookProfile
from api.views import APIAuthView

from django.db.models import Q

class GetCollectionList(APIAuthView):
	def process(self, request):
		parent_pk = request.POST.get('parent_pk', None) or request.POST.get('pk', None)
		if parent_pk is not None:
			try:
				collection = Collection.objects.get(Q(pk=parent_pk)& (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
				self.data['collections'] = []
				for c in collection.children.all():
					self.data['bookshelves'].append({
						'pk': c.pk,
						'name': c.name,
						'parent': c.parent.pk if c.parent is not None else None,
						'slug': c.slug,
						'description': c.description,
						'url': c.get_absolute_url() if c.collection_type != 'series' else None,
						'added': str(c.added),
						'last_modified': str(c.last_modified),
					})
				self.data['meta']['success'] = True
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "Library not found with that pk, for that user"
		else:
			self.data['collections'] = []
			for c in self.user.libraries.all():
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
				self.data['collection'] = {
					'pk': c.pk,
					'name': c.name,
					'parent': c.parent.pk if c.parent is not None else None,
					'description': c.description,
					'url': c.get_absolute_url() if c.collection_type != 'series' else None,
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
				c = Collection.objects.get(Q(pk=collection_id)& (Q(collection__owner=self.user) | Q(collection__parent__owner=self.user) | Q(collection__parent__parent__owner=self.user)))
				self.data['profiles'] = []
				for p in c.books.all():
					self.data['profiles'].append({
						'collection': p.collection.pk,
						'book': p.book_instance.pk,
						'added': str(p.added),
						'last_modified': str(p.last_modified),
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
					'url': p.get_absolute_url(),
				}
				self.data['meta']['success'] = True
						
			except BookProfile.DoesNotExist:
				self.data['meta']['error'] = "BookProfile with that primary key does not exist, for this user"
		
		else:
			self.data['meta']['error'] = "profile_pk not found"

get_collection_list = GetCollectionList()
get_collection_detail = GetCollectionDetail()
get_profile_list = GetBookProfileList()
get_profile_detail = GetBookProfileDetail()