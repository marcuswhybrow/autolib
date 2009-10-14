import os, sys

sys.path.append('/home/marcus')

os.environ['DJANGO_SETTINGS_MODULE'] = 'autolib.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
