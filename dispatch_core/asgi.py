"""
Asynchronous Server Gateway Interface configuration for the
DispatchDjango project.

This module exposes the Asynchronous Server Gateway Interface callable
as a module-level variable named 'application'.
It allows the web server to
communicate with the Django application for handling asynchronous
requests, such as WebSockets or asynchronous HTTP.
"""

import os

from django.core.asgi import get_asgi_application

# Set the default settings module for the 'django-admin' utility.
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'dispatch_core.settings'
)

# Initialize the Asynchronous Server Gateway Interface application.
application = get_asgi_application()
