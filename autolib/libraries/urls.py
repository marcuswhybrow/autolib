from django.conf.urls.defaults import *

from libraries import views

urlpatterns = patterns('libraries.views',
	
	url(r'^$', 'profile', name='profile'),
	url(r'^addbooks/$', 'add_books', name='add_books'),
	url(r'^libraries/$', 'library_list', {'template_name': 'libraries/library_list.html'}, name='library_list'),
	url(r'^libraries/(?P<library_name>[^/]+)/$', 'library_detail', name='library_detail'),
	url(r'^libraries/(?P<library_name>[^/]+)/(?P<bookshelf_name>[^/]+)/$', 'bookshelf_detail', name='bookshelf_detail'),
	url(r'^libraries/(?P<library_name>[^/]+)/(?P<bookshelf_name>[^/]+)/(?P<book_isbn>[^/]+)/(?P<book_title>[^/]*)/?$', 'profile_detail', name='profile_detail'),
)