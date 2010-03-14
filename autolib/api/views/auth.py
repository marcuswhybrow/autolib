# api.views.auth

from django.contrib import auth
from django.contrib.sessions.models import Session

from api.views import APIView, APIAuthView

class AuthGetToken(APIView):
	
	def process(self, request):
		if request.user and request.user.is_authenticated():
			self.data['token_id'] = request.session._get_session_key()
			self.data['meta']['success'] = True
		else:
		
			username = request.POST.get('username', None) or request.POST.get('u', None)
			password = request.POST.get('password', None) or request.POST.get('p', None)
			
			if username is not None and password is not None:
				user = auth.authenticate(username=username, password=password)
				if user is not None and user.is_active:
					auth.login(request, user)
					
					self.data['token_id'] = request.session._get_session_key()
					
					self.data['meta']['success'] = True
			else:
				self.data['meta']['error'] = "Username and Password not found in POST data"

class AuthDestroyToken(APIAuthView):
	
	def process(self, request):
		try:
			if self.token_id is not None:
				session = Session.objects.get(session_key=self.token_id)
			else:
				session = Session.objects.get(session_key=request.session._get_session_key())
			session.delete()
			self.data['meta']['success'] = True
				
		except Session.DoesNotExist:
			self.data['meta']['error'] = "Invalid token"
			

auth_get_token = AuthGetToken()
auth_destroy_token = AuthDestroyToken()