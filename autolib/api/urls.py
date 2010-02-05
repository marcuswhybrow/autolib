
# api urls.py

from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
	
	url(r'^test/$', 'test', name='api_test'),
	
	url(r'^auth/get_token/$', 'auth_get_token', name='api_auth_get_token'),
	url(r'^auth/destroy_token/$', 'auth_destroy_token', name='api_auth_destroy_token'),

	url(r'^libraries/$', 'get_libraries', name='api_get_libraries'),
)