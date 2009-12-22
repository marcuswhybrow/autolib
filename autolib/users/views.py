from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext

def user_detail(request, username):
	return render_to_response('users/user_detail.html', {
		'user_detail': get_object_or_404(User, username=username),
	}, context_instance=RequestContext(request))

def user_list(request):
	return render_to_response('users/user_list.html', {
		'users': User.objects.all()
	})