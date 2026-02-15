"""
Main URL configuration for the DispatchDjango project.
Routes requests to the admin panel and the dispatch_app.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('dispatch_app.urls')),
]
