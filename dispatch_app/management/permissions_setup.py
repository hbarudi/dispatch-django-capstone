"""
Logic for setting up application-specific groups and permissions.
Automates the creation of Reader, Editor, and Journalist groups to
ensure the application meets the security requirements out of the box.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_application_groups(sender, **kwargs):
    """
    Creates the default user groups and
    assigns the required permissions.

    This function is triggered as a post-migration signal, ensuring that
    whenever the database schema is updated, the necessary groups exist.

    Note: The 'sender' and 'kwargs' parameters are required by the
    Django signal API.
    We use them here to satisfy the function signature.
    """
    # These references prevent 'unused' warnings in some
    # IDE configurations
    _ = sender
    __ = kwargs
    # Import models inside the function to avoid circular import issues
    from dispatch_app.models import Article, Newsletter, Publisher

    # Define roles and their corresponding permission codenames
    # Reader: Can only view
    # Editor: Can view, change (update), and delete
    # Journalist: Can add (create), view, change, and delete
    roles_permissions = {
        'Reader': {
            Article: ['view_article'],
            Newsletter: ['view_newsletter'],
        },
        'Editor': {
            Article: ['view_article', 'change_article', 'delete_article'],
            Newsletter: [
                'view_newsletter', 'change_newsletter', 'delete_newsletter'
            ],
            # Added permissions so Editors can manage the Publisher list
            Publisher: ['add_publisher', 'change_publisher', 'view_publisher'],
        },
        'Journalist': {
            Article: [
                'add_article', 'view_article', 'change_article',
                'delete_article'
            ],
            Newsletter: [
                'add_newsletter', 'view_newsletter',
                'change_newsletter', 'delete_newsletter'
            ],
        },
    }

    for group_name, models_perms in roles_permissions.items():
        # Retrieve or create the group
        group, created = Group.objects.get_or_create(name=group_name)

        for model, perms in models_perms.items():
            # Get the Content Type for the model to
            # link permissions correctly
            content_type = ContentType.objects.get_for_model(model)

            for perm_code in perms:
                try:
                    # Find the specific permission object
                    # in the database
                    permission = Permission.objects.get(
                        codename=perm_code,
                        content_type=content_type,
                    )
                    # Assign the permission to the group
                    group.permissions.add(permission)
                # noinspection PyUnresolvedReferences
                except Permission.DoesNotExist:
                    # Logging a warning if a permission isn't found
                    print(
                        f"Warning: Permission {perm_code} "
                        f"not found for {model.__name__}"
                    )

        if created:
            print(f"Successfully created group: {group_name}")
