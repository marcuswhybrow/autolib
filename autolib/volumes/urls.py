##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from django.conf.urls.defaults import *
from volumes.models import Book

import views

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^(?P<page>\d+)?/?$', views.book_list, name='book_list'),
	url(r'^isbn/(?P<isbn>[^/]+)/?$', views.book_detail, name='book_detail'),
)