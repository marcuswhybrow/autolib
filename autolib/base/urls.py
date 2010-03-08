# !Imports

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('base.views',

	# !Views
	url(r'^$', 'index', name='home'),
	url(r'^apps/$', 'direct_to_template', {'template': 'base/apps.html'}, name='apps'),
)