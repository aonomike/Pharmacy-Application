import os, sys

sys.path.append('D:/PROJECTS/DJANGO/venv/ARVDispenser')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ARVDispenser.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()