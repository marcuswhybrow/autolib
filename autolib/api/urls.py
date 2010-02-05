
# api urls.py

from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
	
	url(r'^test/$', 'test', name='api_test'),
	
	url(r'^auth/get_token/$', 'auth_get_token', name='api_auth_get_token'),
	url(r'^auth/destroy_token/$', 'auth_destroy_token', name='api_auth_destroy_token'),

	url(r'^libraries/$', 'get_library_list', name='api_get_library_list'),
	url(r'^libraries/(?P<library_id>\d+)/$', 'get_library_detail', name='api_get_library_detail'),
	url(r'^libraries/(?P<library_id>\d+)/books/$', 'get_library_book_list', name='api_get_library_book_list'),
	url(r'^libraries/(?P<library_id>\d+)/bookshelves/$', 'get_bookshelf_list', name='api_get_bookshelf_list'),
	
	url(r'^bookshelves/(?P<bookshelf_id>\d+)$', 'get_bookshelf_detail', name='api_get_bookshelf_detail'),
	url(r'^bookshelves/(?P<bookshelf_id>\d+)/books/$', 'get_bookshelf_book_list', name='api_get_series_list'),
	url(r'^bookshelves/(?P<bookshelf_id>\d+)/series/$', 'get_series_list', name='api_get_series_list'),
	
	url(r'^series/(?P<series_id>\d+)$', 'get_series_detail', name='api_get_series_detail'),
	url(r'^series/(?P<series_id>\d+)/books/$', 'get_series_book_list', name='api_get_series_list'),
)