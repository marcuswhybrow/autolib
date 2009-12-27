from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', views.library_list, {'template_name': 'libraries/library_list.html'}, name='library_list'),
	url(r'^(?P<library_name>[^/]+)/$', views.library_detail, name='library_detail'),
	url(r'^(?P<library_name>[^/]+)/(?P<bookshelf_name>[^/]+)/$', views.bookshelf_detail, name='bookshelf_detail'),
	url(r'^(?P<library_name>[^/]+)/(?P<bookshelf_name>[^/]+)/(?P<book_isbn>\d+)/[^/]+/$', views.book_detail, name='book_detail'),
)