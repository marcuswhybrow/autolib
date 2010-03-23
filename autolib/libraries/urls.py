from django.conf.urls.defaults import *

from libraries import views
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('libraries.views',
	
	url(r'^$', 'profile', name='profile'),
	url(r'^edit/$', 'profile_edit', name='edit_profile'),
	url(r'^edit/saved/$', direct_to_template, {'template': 'libraries/profile_edit_saved.html'}, name='edit_profile_saved'),
	
	url(r'^addbooks/$', 'add_books', name='add_books'),
	url(r'^libraries/$', 'library_list', {'template_name': 'libraries/library_list.html'}, name='library_list'),
	url(r'^libraries/(?P<library_name>[^/]+)/$', 'library_detail', name='library_detail'),
	url(r'^libraries/(?P<library_name>[^/]+)/(?P<bookshelf_name>[^/]+)/$', 'bookshelf_detail', name='bookshelf_detail'),
	url(r'^libraries/(?P<library_name>[^/]+)/(?P<bookshelf_name>[^/]+)/(?P<book_isbn>[^/]+)/(?P<book_title>[^/]*)/?$', 'profile_detail', name='profile_detail'),
)