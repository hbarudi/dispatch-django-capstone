"""
Configuration module for the dispatch_app.
"""

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class DispatchAppConfig(AppConfig):
    """
    Configuration class for the dispatch_app Django application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dispatch_app'

    def ready(self):
        """
        Executed when the application starts.
        Connects signals and permission setups.
        """
        from .management.permissions_setup import create_application_groups
        post_migrate.connect(create_application_groups, sender=self)

        # Import signals to ensure they are registered with Django
        import dispatch_app.signals  # noqa: F401
