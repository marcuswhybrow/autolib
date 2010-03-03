from api import utils
from django.http import HttpResponse
import simplejson

class APIView(object):
	
	class Meta:
		abstract = True
	
	def __call__(self, request, *args, **kwargs):
		self.data = {'meta': {'success': False}}
		try:
			self.process(request, *args, **kwargs)
		except Exception, e:
			self.data = {'meta': {'success': False, 'error': str(e)}}
		return HttpResponse(simplejson.dumps(self.data), mimetype='application/json')
	
	def prcoess(self, request, *args, **kwargs):
		raise NotImplementedError

class APIAuthView(APIView):
	
	class Meta:
		abstract = True
	
	def __call__(self, request, *args, **kwargs):
		
		self.data = {'meta': {'success': False}}
		self.token_id = request.POST.get('token_id', None)
		self.user = utils.get_user_from_token(self.token_id) if self.token_id is not None else request.user
		
		if self.user and self.user.is_authenticated():
			try:
				self.process(request, *args, **kwargs)
			except Exception, e:
				self.data = {'meta': {'success': False, 'error': str(e)}}
		else:
			self.data['meta']['error'] = 'Invalid token_id'
		
		return HttpResponse(simplejson.dumps(self.data), mimetype='application/json')