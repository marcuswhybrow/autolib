##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from django.http import Http404

def check_user(self, user1, user2):
	if user1 != user2:
		raise Http404 
	
class CurrentUser(object):
	'''
	Ensures that the username argument is the same as the username
	stored in the variable request.username
	'''
	
	def __init__(self, f):
		self.f = f

	def __call__(self, request, username, *args, **kwargs):
		if username != request.user.username:
			raise Http404
		else:
			return self.f(request, username, *args, **kwargs)
	