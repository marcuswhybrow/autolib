import os, sys
import django.core.handlers.wsgi

sys.path.append(r'/home/marcus/autolib/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

sys.stdout = sys.stderr # Prevent crashes upon print

application = django.core.handlers.wsgi.WSGIHandler()