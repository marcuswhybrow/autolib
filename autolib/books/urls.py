from django.conf.urls.defaults import *
from voting.views import vote_on_object
from books.models import Book

import views

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', views.book_list, name='book_list'),
	url(r'^(?P<isbn>\d+)/$', views.book_detail, name='book_detail'),
	url(r'^(?P<object_id>[^/]+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, {
		'model': Book,
		'template_object_name': 'book',
		'allow_xmlhttprequest': True,
	}, name='book_vote'),
)