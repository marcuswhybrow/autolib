# !Imports

from django.conf.urls.defaults import *

urlpatterns = patterns('base.views',

	# !Views
	url(r'^$', 'index', name='home'),
)