from django.db import models
import decimal


class gold_price_config(models.Model):
    gpc_id = models.AutoField(primary_key=True)
    gpc_code = models.CharField(max_length=50)  # price code BUY1, SELL1, BUY2, SELL2
    gpc_description = models.CharField(
        max_length=255
    )  # BUY1 = Harga beli emas senin, SELL1 = Harga jual emas
    gold_price_weight = models.IntegerField()  # berat emas 1
    gold_price_setting_model_buy_weekday = (
        models.CharField()
    )  # base_price + 10 (additionalPrice) + 10 (additional2) + 10(additional3)
    gold_price_setting_model_sell_weekday = (
        models.CharField()
    )  # base_price + 10 (additionalPrice) + 10 (additional2) + 10(additional3)
    gold_price_setting_model_buy_weekend = (
        models.CharField()
    )  # base_price + 10 (additionalPrice) + 10 (additional2) + 10(additional3)
    gold_price_setting_model_sell_weekend = (
        models.CharField()
    )  # base_price + 10 (additionalPrice) + 10 (additional2) + 10(additional3)

    gpc_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=255)
    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.CharField(max_length=255)

    def __str__(self):
        return f"GPC {self.gpc_id} - Weight: {self.gold_price_weight}"

    def calculate_price(self, types: str, base_price: float) -> decimal.Decimal:
        switch = {
            # The line `"BUYWEEKDAY": self.gold_price_setting_model_buy_weekday,` is creating a
            # key-value pair in a dictionary called `switch`. The key is `"BUYWEEKDAY"` and the value
            # is the value of the `gold_price_setting_model_buy_weekday` attribute of the current
            # instance of the `gold_price_config` class. This dictionary is used to map different
            # types of price calculations based on the `types` parameter passed to the
            # `calculate_price` method.
            "BUYWEEKDAY": self.gold_price_setting_model_buy_weekday,
            "SELLWEEKDAY": self.gold_price_setting_model_sell_weekday,
            "BUYWEEKEND": self.gold_price_setting_model_buy_weekend,
            "SELLWEEKDAY": self.gold_price_setting_model_sell_weekend,
        }
        expression = switch.get(types)
        if expression is None:
            raise ValueError(f"Invalid type: {types}")
        return eval(expression)