"""
Application Programming Interface views for the dispatch_app.
Handles the retrieval and filtering of articles for third-party
clients based on user subscriptions.
"""

from typing import cast
from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Article, CustomUser
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows articles to be viewed.
    Filters results based on the user's subscriptions and optional
    search parameters.
    """
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters the articles to show only those from journalists or
        publishers that the current user has subscribed to.
        """
        # Cast the user to CustomUser for IDE attribute recognition
        user = cast(CustomUser, self.request.user)
        # Capture the 'search' parameter from the URL query string
        search_query = self.request.query_params.get('search')

        # Base queryset: only approved articles
        queryset = Article.objects.filter(is_approved=True)

        # Apply subscription filtering for non-superusers
        if not user.is_superuser:
            queryset = queryset.filter(
                Q(publisher__in=user.subscribed_publishers.all()) |
                Q(author__in=user.subscribed_journalists.all())
            )

        # Apply keyword search if the parameter exists
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        # Ensure unique results and order by the newest first
        return queryset.distinct().order_by('-created_at')
