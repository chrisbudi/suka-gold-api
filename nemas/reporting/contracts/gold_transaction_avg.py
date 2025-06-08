# contracts.py
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class GoldTransactionAVGContract:
    avg_pct: Decimal
    current_gold_price: Decimal
    avg_saving_price: Decimal
    diff: Decimal
