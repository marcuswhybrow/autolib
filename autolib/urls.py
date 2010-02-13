# !Imports

from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	### !RESERVED URLS
	### -------------
	
	# !App base paths
	url(r'^$', 'base.views.index', name='home'),
	
	# !Temp forms
# 	(r'^forms/create_library/', 'libraries.views.create_collection', {'collection_type': 'library'}),
# 	(r'^forms/create_bookshelf/', 'libraries.views.create_collection', {'collection_type': 'bookshelf'}),
	
	# !Registration App
	(r'^accounts/', include('registration.backends.default.urls')),
	
	# API
	(r'^api/', include('api.urls')),
	
	# Libraries
	(r'^libraries/', include('libraries.urls')),
	
	# Books
	(r'^books/', include('books.urls')),
	
	# Users
	(r'^users/', include('users.urls')),
	
	### !TOOL AND HELPER URLS
	### --------------------
	
	(r'^admin/', include(admin.site.urls)),
	(r'^hooks/', include('googlehooks.urls')),
	
	# !Media static serve
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
