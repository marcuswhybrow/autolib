from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from users import views

user_patterns = patterns('',
	(r'^$', views.user_detail),
	(r'^libraries/', include('libraries.urls')),
)

urlpatterns = patterns('',

	# Enable the Books Application URL paths
	url(r'^$', views.user_list),
	url(r'^(?P<username>[^/]+)/', include(user_patterns)),
)