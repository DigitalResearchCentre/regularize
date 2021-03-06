"""
WSGI config for regularisation1 project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys
APP_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(APP_PATH)
VENV_PATH = os.path.join(ROOT_PATH, 'venv/lib/python2.6/site-packages')

if not VENV_PATH in sys.path:
    sys.path.insert(0, VENV_PATH)

if not ROOT_PATH in sys.path:
    sys.path.insert(0, ROOT_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "regularisation1.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
