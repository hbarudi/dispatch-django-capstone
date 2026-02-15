"""
Serializers for the dispatch_app application.
Converts model instances into JavaScript Object Notation format
and validates incoming data for the Representational State
Transfer Application Programming Interface.
"""

from rest_framework import serializers
from .models import Article, Publisher, CustomUser, Newsletter


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes basic user information for public display.
    """
    class Meta:
        """Meta configuration for UserSerializer."""
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'role']


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializes publisher information.
    """
    class Meta:
        """Meta-configuration for PublisherSerializer."""
        model = Publisher
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializes article information, including nested author and
    publisher details for a comprehensive view.
    """
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        """Meta configuration for ArticleSerializer."""
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 'publisher',
            'is_approved', 'created_at', 'updated_at'
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializes newsletter information for subscribers.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        """Meta configuration for NewsletterSerializer."""
        model = Newsletter
        fields = ['id', 'title', 'content', 'author', 'created_at']
