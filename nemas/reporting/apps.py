from django.apps import AppConfig


class OrderFixConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reporting"

    def ready(self) -> None:
        import order.signals

        return super().ready()
