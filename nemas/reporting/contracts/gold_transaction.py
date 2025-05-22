# contracts.py
from dataclasses import dataclass


@dataclass
class GoldTransactionContract:
    email: str
    user_id: int
    user_name: str
    transaction_date: str
    transaction_id: int
    weight: float
    price: float
    gold_history_price_base: float
    ref_number: str
    transaction_type: str
