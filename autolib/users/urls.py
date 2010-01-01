from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from users import views

bookshelf_detail = patterns('',
	url(r'^$', views.bookshelf_detail, name='bookshelf_detail'),
	url(r'^(?P<book_isbn>\d+)/(?P<book_title>[^/]*)/?$', views.book_detail, name='book_detail'),
)

library_detail = patterns('',
	url(r'^$', views.library_detail, name='library_detail'),
	url(r'^(?P<bookshelf_name>[^/]+)/', include(bookshelf_detail)),
)

library_list = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', views.library_list, {'template_name': 'users/library_list.html'}, name='library_list'),
	url(r'^(?P<library_name>[^/]+)/', include(library_detail)),
)

user_patterns = patterns('',
	(r'^$', views.user_detail),
	(r'^libraries/', include(library_list)),
)

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', views.user_list, name='user_list'),
	url(r'^(?P<username>[^/]+)/', include(user_patterns), name='user_detail'),
)