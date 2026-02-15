"""
Administrative configuration for the dispatch_app.
Defines how models are displayed and managed within the Django
Admin interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Publisher, Article, Newsletter


class CustomUserAdmin(UserAdmin):
    """
    Extends the default UserAdmin to include custom fields like 'role'
    and subscription relationships in the admin dashboard.
    """
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Subscriptions', {
            'fields': (
                'role', 'subscribed_publishers', 'subscribed_journalists'
            )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Subscriptions', {
            'fields': (
                'role', 'subscribed_publishers', 'subscribed_journalists'
            )
        }),
    )


# Registering models to make them visible in the admin panel.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Newsletter)
