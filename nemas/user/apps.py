from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        import user.signals.receiver.mail_user_reset_password  # noqa: F401 - This import is necessary for signal registration
