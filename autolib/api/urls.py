
# api urls.py

from django.conf.urls.defaults import *

getpatterns = patterns('api.views',

	url(r'^libraries/$', 'get_library_list', name='api_get_library_list'),
	url(r'^libraries/(?P<library_id>\d+)/$', 'get_library_detail', name='api_get_library_detail'),
	url(r'^libraries/(?P<library_id>\d+)/bookshelves/$', 'get_library_bookshelf_list', name='api_get_bookshelf_list'),
	
	url(r'^bookshelves/(?P<bookshelf_id>\d+)/$', 'get_bookshelf_detail', name='api_get_bookshelf_detail'),
	url(r'^bookshelves/(?P<bookshelf_id>\d+)/series/$', 'get_series_list', name='api_get_series_list'),
	
	url(r'^series/(?P<series_id>\d+)/$', 'get_series_detail', name='api_get_series_detail'),
	
	url(r'^books/profiles/$', 'get_collection_book_profile_list', name='api_get_collection_book_profile_list'),
	url(r'^books/profiles/(?P<book_profile_id>\d+)/$', 'get_book_profile_detail', name='api_get_book_profile_detail'),
)

insertpatterns = patterns('api.views',

	url(r'^library/$', 'insert_library', name='api_insert_library'),
	url(r'^bookshelf/$', 'insert_bookshelf', name='api_insert_bookshelf'),	
	url(r'^series/$', 'insert_series', name='api_insert_series'),
	
	url(r'^book/$', 'insert_book', name='api_insert_book'),
)

updatepatterns = patterns('api.views',

	url(r'^library/$', 'update_library', name='api_update_library'),
	url(r'^bookshelf/$', 'update_bookshelf', name='api_update_bookshelf'),	
	url(r'^series/$', 'update_series', name='api_update_series'),
	
	url(r'^book/$', 'insert_book', name='api_insert_book'),
)

authpatterns = patterns('api.views',
	
	url(r'^get_token/$', 'auth_get_token', name='api_auth_get_token'),
	url(r'^destroy_token/$', 'auth_destroy_token', name='api_auth_destroy_token'),
)

syncpatterns = patterns('api.views',
	
	url(r'^update/$', 'sync_update', name='api_sync_update')
)

urlpatterns = patterns('api.views',

	(r'^auth/', include(authpatterns)),
	(r'^get/', include(getpatterns)),
	(r'^insert/', include(insertpatterns)),
	(r'^update/', include(updatepatterns)),
	(r'^sync/', include(syncpatterns)),

)