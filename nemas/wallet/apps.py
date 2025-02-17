from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wallet"

    def ready(self) -> None:
        import wallet.signals

        return super().ready()
