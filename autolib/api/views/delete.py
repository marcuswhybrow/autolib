from volumes.models import BookProfile
from libraries.models import Collection

from api.views import APIAuthView
from django.db.models import Q

class DeleteCollection(APIAuthView):
	def process(self, request):
		collection_pk = request.POST.get('pk', None)
		if collection_pk is not None:
			try:
				c = Collection.objects.get(Q(pk=collection_pk) & (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
				if not c.children.all():
					if not c.books.all():
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
						c.delete()
						self.data['meta']['success'] = True
					else:
						self.data['meta']['error'] = "This Collection cannot be deleted as it contains books"
				else:
					self.data['meta']['error'] = "This Collection cannot be deleted as it contains child Collections"
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "A Collection with that pk does not exist for this User"
		else:
			self.data['meta']['error'] = "pk not found in POST data"
			
class DeleteBookProfile(APIAuthView):
	def process(self, request):
		profile_pk = request.POST.get('pk', None)
		if profile_pk is not None:
			try:
				profile = BookProfile.objects.get(Q(pk=profile_pk) & (Q(collection__owner=self.user) | Q(collection__parent__owner=self.user) | Q(collection__parent__parent__owner=self.user)))
				self.data['profile'] = {
					'pk': profile.pk,
					'isbn10': profile.isbn10,
					'isbn13': profile.isbn13,
					'title': profile.title,
					'description': profile.description,
					'author': profile.author,
					'publisher': profile.publisher,
					'published': str(profile.published),
					'pages': profile.pages,
					'width': profile.width,
					'height': profile.height,
					'depth': profile.depth,
					'format': profile.format,
					'language': profile.language,
					'added': str(profile.added),
					'last_modified': str(profile.last_modified),
					'edition_group': profile.edition_group.pk,
					'url': profile.get_absolute_url(),
					'thumbnail_large': profile.thumbnail_large,
					'thumbnail_small': profile.thumbnail_small,
				}
				profile.delete()
				self.data['meta']['success'] = True
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "A Profile with that pk does not exist for this User"
		else:
			sellf.data['meta']['error'] = "profile_pk not found"

delete_collection = DeleteCollection()
delete_profile = DeleteBookProfile()
