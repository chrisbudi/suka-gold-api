from django.apps import AppConfig


class AuthExtraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_core"

    def ready(self) -> None:

        return super().ready()
