"""
Web Server Gateway Interface configuration for the
DispatchDjango project.

This module exposes the Web Server Gateway Interface callable as
a module-level variable named 'application'.
It allows the web server to communicate with the
Django application for handling synchronous requests.
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django-admin' utility.
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'dispatch_core.settings'
)

# Initialize the Web Server Gateway Interface application.
application = get_wsgi_application()
