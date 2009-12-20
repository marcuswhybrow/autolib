from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User

def user_detail(request, username):
	return render_to_response('users/user_detail.html', { 'user_detail': get_object_or_404(User, username=username) })