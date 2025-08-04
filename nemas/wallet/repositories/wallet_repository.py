from user.api.views.user_prop_view import UserProps
from django.db import transaction
from django.db import transaction
from wallet.models import wallet_history


class WalletService:
    def __init__(self, wallet_repo):
        self.wallet_repo = wallet_repo

    @transaction.atomic
    def deposit(self, user, amount):
        wallet = self.wallet_repo.get(user)
        wallet.topup(amount)
        self.wallet_repo.save(wallet)

        wallet_history.objects.create(user=user, amount=amount, transaction_type="D")

    @transaction.atomic
    def withdraw(self, user, amount):
        wallet = self.wallet_repo.get(user)
        wallet.withdraw(amount)
        self.wallet_repo.save(wallet)

        wallet_history.objects.create(user=user, amount=amount, transaction_type="W")
