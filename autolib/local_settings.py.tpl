import os

WORKING_COPY = True
PATH = os.path.abspath(os.path.dirname(__file__))

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PATH, 'dev.db')

MEDIA_URL = '/media/'

GOOGLEHOOKS_PROJECTS = {
	'autolib': ('post-commit key', 'command to run'),
}

GOOGLEHOOKS_LOGFILE = 'google hooks log'