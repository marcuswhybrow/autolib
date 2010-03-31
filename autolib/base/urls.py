##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('base.views',

	# !Views
	url(r'^$', 'index', name='home'),
	url(r'^apps/$', 'direct_to_template', {'template': 'base/apps.html'}, name='apps'),
)