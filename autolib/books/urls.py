from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', views.book_list, name='book_list'),
	url(r'^(?P<isbn>\d+)/$', views.book_detail, name='book_detail'),
)