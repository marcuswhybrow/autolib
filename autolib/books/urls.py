from django.conf.urls.defaults import *

library_patterns = patterns('autolib.books.views',
	(r'^$', 'library_detail'),
	(r'^(?P<bookshelf_name>(^/)+)/', 'bookshelf_detail')
)

urlpatterns = patterns('autolib.books.views',

	# Enable the Books Application URL paths
	(r'^$', 'libraries'),
	(r'^(?P<library_name>(^/)+)/', include(library_patterns)),
)