from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	(r'^books/', include("autolib.books.urls")),

	# Enables the Profile View
	(r'^profile/', 'autolib.books.views.profile'),

	# Enables the Library List (Index) View
	(r'^$', 'autolib.books.views.library_list'),
	
	# Enable the admin URL paths
	(r'^admin/', include(admin.site.urls)),
)
