from django.conf.urls.defaults import *

urlpatterns = patterns('users.views',
	
	url(r'^$', 'user_list', name='user_list'),
	url(r'^(?P<username>[^/]+)/$', 'user_detail', name='user_detail'),
)