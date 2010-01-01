# !Imports

from django.conf.urls.defaults import *

apipatterns = patterns('base.views',
	(r'^$', 'hello_world_service'),
	(r'^service.wsdl', 'hello_world_service'),
	(r'^wsdl/', 'wsdl_doc'),
)

urlpatterns = patterns('base.views',

	# !Views
	url(r'^$', 'index', name='home'),

	# !SOAP
	(r'^api/', include(apipatterns)),
)