"""
Models for the dispatch_app application.
Defines the structure for Users, Publishers, Articles, and Newsletters.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model supporting roles: Reader, Editor, and Journalist.
    Includes subscription fields for readers and publication tracking
    for journalists.
    """
    objects = models.Manager()

    ROLE_CHOICES = (
        ('READER', 'Reader'),
        ('EDITOR', 'Editor'),
        ('JOURNALIST', 'Journalist'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='READER'
    )

    # Reader-specific fields (Subscriptions)
    subscribed_publishers = models.ManyToManyField(
        'Publisher',
        blank=True,
        related_name='subscribers'
    )
    subscribed_journalists = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='journalist_subscribers'
    )

    def __str__(self):
        """Returns the string representation of the user."""
        return f"{self.username} ({self.role})"


class Publisher(models.Model):
    """
    Represents a news organization or publishing entity.
    Can have multiple affiliated editors and journalists.
    """
    objects = models.Manager()

    name = models.CharField(max_length=255)
    editors = models.ManyToManyField(
        CustomUser,
        related_name='managed_publishers',
        limit_choices_to={'role': 'EDITOR'}
    )
    journalists = models.ManyToManyField(
        CustomUser,
        related_name='publisher_affiliations',
        limit_choices_to={'role': 'JOURNALIST'}
    )

    def __str__(self):
        """Returns the name of the publisher."""
        return self.name


class Article(models.Model):
    """
    Represents a news article written by a journalist.
    Requires editor approval before becoming visible to readers.
    """
    objects = models.Manager()

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles',
        limit_choices_to={'role': 'JOURNALIST'}
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the title of the article."""
        return self.title


class Newsletter(models.Model):
    """
    Represents a newsletter distributed to subscribers.
    """
    objects = models.Manager()

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='newsletters'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the title of the newsletter."""
        return self.title
