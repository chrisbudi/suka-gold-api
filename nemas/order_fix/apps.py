from django.apps import AppConfig


class OrderFixConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order_fix"

    def ready(self) -> None:

        return super().ready()
