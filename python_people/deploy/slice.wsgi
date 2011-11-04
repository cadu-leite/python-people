import os
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, '/usr/local/venvs/python_people/lib/python2.5/site-packages')
sys.path.insert(0, abspath(join(dirname(__file__), "../")))

sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

os.environ['DJANGO_SETTINGS_MODULE'] = 'python_people.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()