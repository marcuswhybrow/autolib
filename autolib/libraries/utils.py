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

class Adapter(object):
	"""
	An interface for other adapters
	"""
	
	def __init__(self, isbn):
		raise NotImplementedError
	
	def get_name(self):
		raise NotImplementedError
	
	def get_isbn(self):
		raise NotImplementedError
		
	def get_name(self):
		raise NotImplementedError
	
	def get_description(self):
		raise NotImplementedError
	
	def get_publisher(self):
		raise NotImplementedError
	
	def get_published(self):
		raise NotImplementedError
	
	def get_author(self):
		raise NotImplementedError
	
	def get_length(self):
		raise NotImplementedError

class GoogleAdapter(Adapter):
	"""
	Gets information regarding books using Google's books API
	"""
	
	def __init__(self, isbn):
		pass
	
	def get_name(self):
		pass
		
	def get_isbn(self):
		pass
		
	def get_name(self):
		pass
	
	def get_description(self):
		pass
	
	def get_publisher(self):
		pass
	
	def get_published(self):
		pass
	
	def get_author(self):
		pass
	
	def get_length(self):
		pass
	