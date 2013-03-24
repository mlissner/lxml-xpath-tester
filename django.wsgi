import os
import sys

# See https://modwsgi.readthedocs.org/en/latest/application-issues/index.html#non-blocking-module-imports
import _strptime

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

sys.path.append('/var/www/xpathtester')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
