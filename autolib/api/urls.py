##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from django.conf.urls.defaults import *

authpatterns = patterns('api.views.auth',
	
	url(r'^get_token/?$', 'auth_get_token', name='api_auth_get_token'),
	url(r'^destroy_token/?$', 'auth_destroy_token', name='api_auth_destroy_token'),
)

syncpatterns = patterns('api.views.sync',
	
	url(r'^update/?$', 'sync_update', name='api_sync_update')
)

getpatterns = patterns('api.views.get',

	url(r'^collections/?$', 'get_collection_list', name='api_get_collection_list'),
	url(r'^collection/?$', 'get_collection_detail', name='api_get_collection_detail'),
	
	url(r'^profiles/?$', 'get_profile_list', name='api_get_profile_list'),
	url(r'^profile/?$', 'get_profile_detail', name='api_get_profile_detail'),
	
	url(r'^book/?', 'get_book_detail', name='api_get_book_detail'),
	
	url(r'^user/?', 'get_user_detail', name='api_get_user_detail'),
)

savepatterns = patterns('api.views.save',

	url(r'^collection/?$', 'save_collection', name='api_save_collection'),
	url(r'^profile/?$', 'save_profile', name='api_save_profile'),
)

deletepatterns = patterns('api.views.delete',

	url(r'^collection/?$', 'delete_collection', name='api_delete_collection'),
	url(r'^profile/?$', 'delete_profile', name='api_delete_profile'),
)

urlpatterns = patterns('api.views',

	(r'^auth/', include(authpatterns)),
	(r'^get/', include(getpatterns)),
	(r'^save/', include(savepatterns)),
	(r'^sync/', include(syncpatterns)),
	(r'^delete/', include(deletepatterns)),

)