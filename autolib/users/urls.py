##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from django.conf.urls.defaults import *

urlpatterns = patterns('users.views',
	
	url(r'^$', 'user_list', name='user_list'),
	url(r'^(?P<username>[^/]+)/$', 'user_detail', name='user_detail'),
)