from django.conf.urls.defaults import *
#from autolib.books.models import Book
#
#info_dict = {
#	'queryset' : Book.objects.all()
#}
#
#urlpatterns = patterns('',
#	(r'^$', 'django.views.generic.list_detail.object_list', info_dict),
#	(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
#	(r'^add/$', 'autolib.books.views.book_add'),
#	(r'^add/handler/$', 'autolib.books/views/book_add_handler'),
#)


urlpatterns = patterns('autolib.books.views',

	# Enable the Books Application URL paths
	(r'^$', 'index'),
	(r'^(?P<isbn>\d+)/$', 'book'),
	(r'^add/$', 'book_add'),
	(r'^add/handler/$', 'book_add_handler'),
)
