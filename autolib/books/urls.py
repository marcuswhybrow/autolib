from django.conf.urls.defaults import *

urlpatterns = patterns('autolib.books.views',

	# Enable the Books Application URL paths
	(r'^$', 'libraries'),
	(r'^(?P<library_name>(^/)+)/', 'library_detail'),
	(r'^(?P<library_name>(^/)+)/(?P<bookshelf_name>(^/)+)/', 'bookshelf_detail'),
)