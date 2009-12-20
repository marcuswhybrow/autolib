import os, sys

sys.path.append(r'/home/marcus')

os.environ['DJANGO_SETTINGS_MODULE'] = 'autolib.settings'

sys.stdout = sys.stderr # Prevent crashes upon print

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()