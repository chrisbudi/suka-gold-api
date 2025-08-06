class GoldTransactionService:
    def __init__(self, wallet_service, gold_service, price_provider, system_user):
        self.wallet_service = wallet_service
        self.gold_service = gold_service
        self.price_provider = price_provider
        self.system_user = system_user  # <- platform account

    def buy_gold(self, user, grams):
        """User buys gold from platform."""
        price = self.price_provider.get_price()
        total_cost = grams * price

        # 1. User pays money
        self.wallet_service.withdraw(user, total_cost)

        # 2. Platform receives money
        self.wallet_service.deposit(self.system_user, total_cost)

        # 3. Platform gives gold to user
        self.gold_service.reduce_gold(
            self.system_user,
            grams,
            price_base=price,
            price_sell=price,
            amount=total_cost,
        )

        # 4. User receives gold
        self.gold_service.add_gold(
            user, grams, price_base=price, price_buy=price, amount=total_cost
        )

    def sell_gold(self, user, grams):
        """User sells gold to platform."""
        price = self.price_provider.get_price()
        total_value = grams * price

        # 1. User gives gold to platform
        self.gold_service.reduce_gold(
            user, grams, price_base=price, price_sell=price, amount=total_value
        )

        self.gold_service.add_gold(
            self.system_user,
            grams,
            price_base=price,
            price_buy=price,
            amount=total_value,
        )

        # 2. Platform pays money
        self.wallet_service.withdraw(self.system_user, total_value)

        # 3. User receives money
        self.wallet_service.deposit(user, total_value)
