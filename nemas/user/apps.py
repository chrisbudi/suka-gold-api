import sys
from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        import user.signals.receiver.mail_user_reset_token  # noqa: F401 - This import is necessary for signal registration

        if "migrate" not in sys.argv and "makemigrations" not in sys.argv:
            from shared_kernel.utils.system_user import get_system_user

            get_system_user()
