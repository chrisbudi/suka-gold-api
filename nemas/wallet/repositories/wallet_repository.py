from decimal import Decimal
from user.api.views.user_prop_view import UserProps
from django.db import transaction
from django.db import transaction
from wallet.models import wallet, wallet_history

from django.core.exceptions import ValidationError


class WalletRepository:
    def __init__(self, user=None):
        self.user = user

    @transaction.atomic
    def deduct_balance(self, amount: Decimal, notes=None):
        walletObject = wallet.objects.select_for_update().get(user=self.user)
        if walletObject.balance < amount:
            raise ValidationError("Insufficient wallet balance")
        walletObject.balance -= amount
        walletObject.save()

        wallet_history.objects.create(
            user=self.user, amount=-amount, type="D", notes=notes
        )

    @transaction.atomic
    def add_balance(self, amount: Decimal, notes=None):
        walletObj = wallet.objects.select_for_update().get(user=self.user)
        walletObj.balance += amount
        walletObj.save()

        wallet_history.objects.create(
            user=self.user, amount=amount, type="C", notes=notes
        )

    def get_wallet_balance(self, user_id):
        try:
            walletObject = wallet.objects.get(user_id=user_id)
            return walletObject.balance
        except wallet.DoesNotExist:
            raise ValidationError("Wallet does not exist for this user")
