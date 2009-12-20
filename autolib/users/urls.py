from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from users import views

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', direct_to_template, {'template': 'users/user_list.html'}),
	url(r'^(?P<username>[^/]+)/$', views.user_detail),
)