from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	### RESERVED URLS
	### -------------
	
	# Site root - Enables the Library List (Index) View
	(r'^$', direct_to_template, {'template': 'books/index.html'}),

	# Enables the Books Application URL paths
	(r'^libraries/', include('libraries.urls')),
	
	# Enable the Users Application URL paths
	(r'^users/', include('autolib.users.urls')),
	
	# User stuff
	(r'^accounts/', include('registration.backends.default.urls')),
# 	(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'books/login.html'}),
	
	### TOOL AND HELPER URLS
	### --------------------
	
	# Enable the admin URL paths
	(r'^admin/', include(admin.site.urls)),
	
	# Enable googlehooks
	(r'^hooks/', include('autolib.googlehooks.urls')),

	# SOAP test
	(r'^api/', 'autolib.libraries.views.hello_world_service'),
	(r'^api/service.wsdl', 'autolib.libraries.views.hello_world_service'),
	(r'^api/wsdl/', 'autolib.libraries.views.wsdl_doc'),

	# Enable media from the same website
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
