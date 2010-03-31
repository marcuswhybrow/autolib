##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

from base.models import Config

def user(request):
	'''
	Adds the user to the request context,
	in addition adds all configuration records to the context.
	In a template a config would be access via "unsorted_bin.value" or "unsorted_bin.slug" for example,
	if the key of the config was "unsorted_bin"
	'''
	
	context = {'user': request.user}
	for config in Config.objects.all():
		context[config.key] = config
	return context