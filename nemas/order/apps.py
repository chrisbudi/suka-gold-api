from django.apps import AppConfig


class GoldTransactionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order"

    def ready(self) -> None:
        # import order.signals

        return super().ready()
