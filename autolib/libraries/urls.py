from django.conf.urls.defaults import *

import views

bookshelf_patterns = patterns('',
	url(r'^$', views.bookshelf_detail, name='bookshelf_detail'),
	url(r'^(?P<book_isbn>\d+)/(?P<book_title>[^/]*)/$', views.book_detail, name='book_detail'),
)

library_patterns = patterns('',
	url(r'^$', views.library_detail, name='library_detail'),
	url(r'^(?P<bookshelf_name>[^/]+)/', include(bookshelf_patterns)),
)

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', views.library_list, {'template_name': 'libraries/library_list.html'}, name='library_list'),
	url(r'^(?P<library_name>[^/]+)/', include(library_patterns)),
)