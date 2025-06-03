# contracts.py
from dataclasses import dataclass


@dataclass
class GoldTransactionAVGContract:
    user_id: str
    current_gold_price_buy: float
    current_gold_price_sell: float
    avg_buy_price: float
    avg_sell_price: float
    percentage_from_sell: float
    percentage_from_buy: float
