"""
Signals for the dispatch_app application.
Handles automated tasks like email notifications and X integration
when an article is approved.
"""

import requests
from requests_oauthlib import OAuth1
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Article


@receiver(post_save, sender=Article)
def handle_article_approval(sender, instance, created, **kwargs):
    """
    Triggered whenever an Article is saved.
    If approved, it initiates notifications and social sharing.
    """
    _ = sender
    __ = created
    ___ = kwargs
    # We only care if the article is approved.
    # To prevent duplicate tweets when an approved article is edited,
    # we can check if the approval is the primary change.
    if instance.is_approved:
        # We fetch the version currently in the database to see
        # if it was already approved.
        try:
            old_instance = Article.objects.get(pk=instance.pk)
            # If it was already approved in the database, do nothing.
            if old_instance.is_approved:
                return
        # noinspection PyUnresolvedReferences
        except Article.DoesNotExist:
            # New article being created as already approved
            # (the Admin panel)
            pass

        # If we reached here, it means the article is newly approved.
        send_approval_emails(instance)
        post_to_x(instance)


def send_approval_emails(article):
    """
    Collects recipients and sends an email notification about the
    newly published article.
    """
    # Get subscribers from both the author and the publisher
    recipients = set()

    # Subscribers of the journalist
    journalist_subs = article.author.journalist_subscribers.all()
    for sub in journalist_subs:
        if sub.email:
            recipients.add(sub.email)

    # Subscribers of the publisher
    if article.publisher:
        publisher_subs = article.publisher.subscribers.all()
        for sub in publisher_subs:
            if sub.email:
                recipients.add(sub.email)

    if recipients:
        send_mail(
            f"New Article: {article.title}",
            f"A new article has been published: {article.title}",
            settings.DEFAULT_FROM_EMAIL,
            list(recipients),
            fail_silently=True,
        )


def post_to_x(article):
    """
    Uses the X Application Programming Interface to share the article.
    Requires OAuth1 authentication.
    """
    # Access keys from the settings module
    api_key = settings.X_API_KEY
    api_secret = settings.X_API_SECRET_KEY

    # Access tokens are required for user-context posting
    access_token = getattr(settings, 'X_ACCESS_TOKEN', None)
    access_token_secret = getattr(settings, 'X_ACCESS_TOKEN_SECRET', None)

    # Validate configuration before attempting request
    if api_key == 'your-api-key-here' or not access_token:
        print(f"DEBUG: X API credentials missing for: {article.title}")
        return

    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(api_key, api_secret, access_token, access_token_secret)
    payload = {"text": f"New Dispatch: {article.title}\nRead more now!"}

    try:
        response = requests.post(url, auth=auth, json=payload, timeout=10)
        if response.status_code == 201:
            print(f"SUCCESS: Posted '{article.title}' to X.")
        else:
            # Printing the full response helps diagnose 403 Forbidden errors
            print(
                f"ERROR: X API returned {response.status_code}:"
                f" {response.text} ."
            )
    except requests.exceptions.RequestException as e:
        print(f"CONNECTION ERROR: Could not reach X API: {e}")
