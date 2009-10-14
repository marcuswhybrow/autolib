from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	(r'^books/', include("autolib.books.urls")),

	(r'^profile/', 'autolib.books.views.profile'),

	(r'^$', 'autolib.books.views.library_list'),
	
	# Enable the admin URL paths
	(r'^admin/', include(admin.site.urls)),
)
