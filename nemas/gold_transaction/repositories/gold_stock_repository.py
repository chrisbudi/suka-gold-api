from core.domain.gold import gold_stock


class GoldStockRepository:
    def get_or_create_stock(self, user):
        return gold_stock.objects.get_or_create(user=user)[0]

    def add_weight(self, user, weight):
        stock = self.get_or_create_stock(user)
        stock.topup_stock += weight
        stock.save()
        return stock

    def reduce_weight(self, user, weight):
        stock = self.get_or_create_stock(user)
        if stock.topup_stock < weight:
            raise ValueError("Insufficient gold")
        stock.topup_stock -= weight
        stock.save()
        return stock
