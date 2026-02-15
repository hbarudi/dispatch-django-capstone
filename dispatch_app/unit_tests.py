"""
Unit tests for the dispatch_app application.
Specifically tests the RESTful API endpoints and ensures that
article filtering based on subscriptions is functioning correctly.
"""

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Article, Publisher



class ArticleAPITests(APITestCase):
    """
    Test suite for the Article Application Programming Interface.
    """


    def setUp(self):
        """
        Sets up the test environment by creating publishers,
        journalists, readers, and articles.
        """
        # Create a Journalist
        self.journalist = CustomUser.objects.create_user(
            username='journalist1',
            password='Password123!',
            role='JOURNALIST'
        )

        # Create a Publisher
        self.publisher = Publisher.objects.create(name='Global News')

        # Create an Article from this journalist and publisher
        self.article = Article.objects.create(
            title='Test Article',
            content='This is test content.',
            author=self.journalist,
            publisher=self.publisher,
            is_approved=True
        )

        # Create a Reader
        self.reader = CustomUser.objects.create_user(
            username='reader1',
            password='Password123!',
            role='READER'
        )


    def test_unauthenticated_access(self):
        """
        Ensures that unauthenticated users cannot access the API.
        """
        url = reverse('article-api-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_subscription_filtering(self):
        """
        Tests that a reader only sees articles from sources they
        are subscribed to.
        """
        url = reverse('article-api-list')
        self.client.force_authenticate(user=self.reader)

        # Initially, the reader has no subscriptions, should see 0
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

        # Subscribe the reader to the publisher
        self.reader.subscribed_publishers.add(self.publisher)

        # Now the reader should see the article
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Article')


    def test_superuser_access(self):
        """
        Ensures that superusers can see all approved articles
        regardless of subscriptions.
        """
        admin_user = CustomUser.objects.create_superuser(
            username='admin_test',
            password='Password123!',
            email='admin@test.com'
        )
        url = reverse('article-api-list')
        self.client.force_authenticate(user=admin_user)

        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
