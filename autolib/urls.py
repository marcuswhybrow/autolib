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
	url(r'^apps/$', direct_to_template, {'template': 'base/apps.html'}, name='apps'),
	url(r'^apps/android$', direct_to_template, {'template': 'base/apps_android.html'}, name='apps_android'),
	url(r'^apps/java$', direct_to_template, {'template': 'base/apps_java.html'}, name='apps_java'),
	
	# !Registration App
	(r'^accounts/', include('registration.backends.default.urls')),
	
	# API
	(r'^api/', include('api.urls')),
	
	# Profile
	(r'^profile/', include('libraries.urls')),
	
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
