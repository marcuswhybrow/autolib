
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

def get_user_from_token(token_id):
	try:
		session = Session.objects.get(session_key=token_id)
		uid = session.get_decoded().get('_auth_user_id')
		
		try:
			user = User.objects.get(pk=uid)
			if user.is_authenticated():
				return user
				
		except User.DoesNotExist:
			pass
	except Session.DoesNotExist:
		pass
	
	return None
