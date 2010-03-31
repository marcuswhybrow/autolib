##
## Developed for the University of Nottingham G52GRP module
##
## Written by:	Marcus Whybrow (mxw18u)
## Group: 		gp09-drm
##

import os, sys
import django.core.handlers.wsgi

PATH = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(PATH, '..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

sys.stdout = sys.stderr # Prevent crashes upon print

application = django.core.handlers.wsgi.WSGIHandler()