from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	### RESERVED URLS
	### -------------
	
	# Site root - Enables the Library List (Index) View
	(r'^$', 'libraries.views.index'),

	# Enables the Libraries app URL paths
	(r'^libraries/', include('libraries.urls')),
	
	# Enables the Books app URL paths
	(r'^books/', include('books.urls')),
	
	# Enable the Users app URL paths
	(r'^users/', include('users.urls')),
	
	# Expose forms on their own
	(r'^forms/create_library', 'libraries.forms.create_collection', {'collection_type': 'library'}),
	(r'^forms/create_bookshelf', 'libraries.forms.create_collection', {'collection_type': 'bookshelf'}),
	
	# User stuff
	(r'^accounts/', include('registration.backends.default.urls')),
# 	(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'books/login.html'}),
	
	### TOOL AND HELPER URLS
	### --------------------
	
	# Enable the admin URL paths
	(r'^admin/', include(admin.site.urls)),
	
	# Enable googlehooks
	(r'^hooks/', include('googlehooks.urls')),

	# SOAP test
	(r'^api/', 'libraries.views.hello_world_service'),
	(r'^api/service.wsdl', 'libraries.views.hello_world_service'),
	(r'^api/wsdl/', 'libraries.views.wsdl_doc'),

	# Enable media from the same website
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
