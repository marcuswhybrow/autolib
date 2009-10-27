from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
	(r'^post-commit/$', views.post_commit),
)
