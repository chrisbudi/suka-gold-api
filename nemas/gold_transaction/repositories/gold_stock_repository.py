from decimal import Decimal
from gold_transaction.models.gold_stock import gold_history, gold_stock
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from shared_kernel.utils.system_user import get_system_user


class GoldStockRepository:
    def __init__(self, user):
        self.user = user

    def get_or_create_user_stock(self, user):
        stock, _ = gold_stock.objects.get_or_create(user=user)
        return stock

    def get_system_stock(self):
        system_user = get_system_user()
        try:
            return gold_stock.objects.get(user=system_user)
        except ObjectDoesNotExist:
            raise ValueError("System stock not initialized")

    @transaction.atomic
    def buy_gold(
        self, weight: Decimal, price_base: Decimal, price_buy: Decimal, notes: str
    ):

        amount = weight * price_buy
        # Deduct from system
        system_stock = self.get_system_stock()
        system_stock.reduce_gold(weight)
        system_stock.save()

        # Add to user
        user_stock = self.get_or_create_user_stock(self.user)

        user_stock.weight += weight
        user_stock.save()

        # Log history
        gold_history.objects.create(
            user=self.user,
            weight=weight,
            price_base=price_base,
            price_buy=price_buy,
            price_sell=Decimal(0),
            transaction_type="B",
            amount=amount,
            note=notes,
        )

    @transaction.atomic
    def sell_gold(
        self,
        weight: Decimal,
        price_base: Decimal,
        price_sell: Decimal,
        notes: str,
    ):
        amount = weight * price_sell

        user_stock = self.get_or_create_user_stock(self.user)

        # Deduct from user
        user_stock.reduce_gold(weight)
        user_stock.save()

        # Add to system
        system_stock = self.get_system_stock()
        system_stock.weight += weight
        system_stock.save()

        # Log history
        gold_history.objects.create(
            user=self.user,
            weight=weight,
            price_base=price_base,
            price_buy=Decimal(0),
            price_sell=price_sell,
            transaction_type="S",
            amount=amount,
            note=notes,
        )

    @transaction.atomic
    def transfer_gold(self, user_to, weight: Decimal):
        if weight <= 0:
            raise ValueError("Weight must be positive")

        from_stock = self.get_or_create_user_stock(self.user)
        to_stock = self.get_or_create_user_stock(user_to)

        if from_stock.weight < weight:
            raise ValueError("Not enough gold in user's stock")

        # Transfer gold
        from_stock.weight -= weight
        to_stock.weight += weight

        from_stock.save()
        to_stock.save()

        # Log history for both users
        gold_history.objects.create(
            user=self.user,
            weight=weight,
            price_base=Decimal(0),
            price_buy=Decimal(0),
            price_sell=Decimal(0),
            transaction_type="S",
            amount=0,
            note=f"Transfer to {user_to.username}",
        )

        gold_history.objects.create(
            user=user_to,
            weight=weight,
            price_base=Decimal(0),
            price_buy=Decimal(0),
            price_sell=Decimal(0),
            transaction_type="B",
            amount=0,
            note=f"Transfer from {from_stock.user.username}",
        )
