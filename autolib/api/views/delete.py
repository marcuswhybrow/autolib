from books.models import BookProfile
from libraries.models import Collection

from api.views import APIAuthView
from django.db.models import Q

class DeleteCollection(APIAuthView):
	def process(self, request):
		collection_pk = request.POST.get('collection_pk', None) or request.POST.get('pk', None)
		if collection_pk is not None:
			try:
				collection = Collection.objects.get(Q(pk=collection_pk) & (Q(owner=self.user) | Q(parent__owner=self.user) | Q(parent__parent__owner=self.user)))
				if not collection.children.all():
					if not collection.books.all():
						self.data['collection'] = {
							'pk': collection.pk
						}
						collection.delete()
						self.data['meta']['success'] = True
					else:
						self.data['meta']['error'] = "This Collection cannot be deleted as it contains books"
				else:
					self.data['meta']['error'] = "This Collection cannot be deleted as it contains child Collections"
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "A Collection with that pk does not exist for this User"
		else:
			self.data['meta']['error'] = "collection_pk not found in POST data"
			
class DeleteBookProfile(APIAuthView):
	def process(self, request):
		profile_pk = request.POST.get('profile_pk', None) or request.POST.get('pk', None)
		if profile_pk is not None:
			try:
				profile = BookProfile.objects.get(Q(pk=profile_pk) & (Q(collection__owner=self.user) | Q(collection__parent__owner=self.user) | Q(collection__parent__parent__owner=self.user)))
				self.data['profile'] = {
					'pk': series.pk
				}
				profile.delete()
				self.data['meta']['success'] = True
			except Collection.DoesNotExist:
				self.data['meta']['error'] = "A Profile with that pk does not exist for this User"
		else:
			sellf.data['meta']['error'] = "profile_pk not found"

delete_collection = DeleteCollection()
delete_profile = DeleteBookProfile()
