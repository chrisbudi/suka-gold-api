from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction
from typing import Optional

UserModel = get_user_model()

_system_user_cache = None


def get_system_user():
    """
    Get or create the system user globally.
    Returns the system user instance or None if creation fails.
    """
    global _system_user_cache

    # Return cached instance if available
    if _system_user_cache is not None:
        return _system_user_cache

    try:
        with transaction.atomic():
            system_user, created = UserModel.objects.get_or_create(
                id=settings.SYSTEM_USER_ID,
                defaults={
                    "user_name": "system",
                    "email": "system@mail.com",
                    "phone_number": "0000000000",
                    "is_active": False,  # System user shouldn't login
                    "is_staff": False,
                    "is_superuser": False,
                    "last_login": None,
                },
            )

            # Cache the system user
            _system_user_cache = system_user

            if created:
                print(f"System user created with ID: {settings.SYSTEM_USER_ID}")

            return system_user

    except Exception as e:
        print(f"Could not get/create system user: {e}")
        return None


def clear_system_user_cache():
    """Clear the cached system user (useful for testing)."""
    global _system_user_cache
    _system_user_cache = None


def get_system_user_id() -> str:
    """Get the system user ID from settings."""
    return settings.SYSTEM_USER_ID
