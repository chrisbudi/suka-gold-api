from django.apps import AppConfig


class GoldTransactionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gold_transaction"

    def ready(self) -> None:
        import gold_transaction.signals

        return super().ready()
