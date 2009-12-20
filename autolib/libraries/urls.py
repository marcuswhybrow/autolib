from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', views.library_list, {'template_name': 'books/library_list.html'}),
	url(r'^(?P<library_name>[^/]+)/$', views.library_detail),
	url(r'^(?P<library_name>[^/]+)/(?P<bookshelf_name>[^/]+)/$', views.bookshelf_detail),
)