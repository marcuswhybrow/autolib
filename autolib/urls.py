from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# Enable media from the same website
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	# Enable the Books Application URL paths
	(r'^books/', include('autolib.books.urls')),

	# Enables the Profile View
	(r'^profile/', 'autolib.books.views.profile'),

	# Enables the Library List (Index) View
	(r'^$', 'autolib.books.views.library_list'),
	
	# Enable the admin URL paths
	(r'^admin/', include(admin.site.urls)),
	
	# Enable googlehooks
	(r'^hooks/', include('autolib.googlehooks.urls')),
	
	# SOAP test
	(r'^api/', 'autolib.books.views.hello_world_service'),
	(r'^api/service.wsdl', 'autolib.books.views.hello_world_service'),
	
	(r'^api/wsdl/', 'autolib.books.views.wsdl_doc'),

)
