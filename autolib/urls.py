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
	#(r'^libraries/', include('libraries.urls')),
	(r'^books/', include('books.urls')),
	(r'^users/', include('users.urls')),
	
	# !Temp forms
	(r'^forms/create_library/', 'users.views.create_collection', {'collection_type': 'library'}),
	(r'^forms/create_bookshelf/', 'users.views.create_collection', {'collection_type': 'bookshelf'}),
	
	# !Registration App
	(r'^accounts/', include('registration.backends.default.urls')),
# 	(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'books/login.html'}),

	(r'^api/', include('api.urls')),
	
	### !TOOL AND HELPER URLS
	### --------------------
	
	(r'^admin/', include(admin.site.urls)),
	(r'^hooks/', include('googlehooks.urls')),
	
	# !Media static serve
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
