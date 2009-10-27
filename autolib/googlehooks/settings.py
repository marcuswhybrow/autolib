"""
Convenience module for access of custom application settings,
which enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

DEFAULT_LOGFILE = '/var/log/googlehooks.log'

"""
Specify your projects thusly:
	
	GOOGLEHOOKS_PROJECTS = {
		'my_project': (<secret_key>, <callable_object_or_command>),
	}
	
"""
GOOGLEHOOKS_PROJECTS = getattr(settings, 'GOOGLEHOOKS_PROJECTS', { })

GOOGLEHOOKS_LOGFILE = getattr(settings, 'GOOGLEHOOKS_LOGFILE', DEFAULT_LOGFILE)
