"""WSGI config for D4 Technologies project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d4.settings")
application = get_wsgi_application()
