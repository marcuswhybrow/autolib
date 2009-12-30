from django.http import Http404

def check_user(self, user1, user2):
	if user1 != user2:
		raise Http404 
	
class CurrentUser(object):
	def __init__(self, orig_func):
		self.orig_func = orig_func

	def __call__(self, request, username, *args, **kwargs):
		if username != request.user.username:
			raise Http404
		else:
			return self.orig_func(request, username, *args, **kwargs)