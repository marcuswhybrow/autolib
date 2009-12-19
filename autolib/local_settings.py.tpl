import os

WORKING_COPY = True
PATH = os.path.abspath(os.path.dirname(__file__))

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PATH, 'dev.db')

MEDIA_URL = '/media/'

# The following is only required if the local machine is the server,
# not for example if this is a working copy.

'''
GOOGLEHOOKS_PROJECTS = {
	'autolib': ('post-commit key', 'command to run'),
}

GOOGLEHOOKS_LOGFILE = 'google hooks log'
'''