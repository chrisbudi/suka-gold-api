# contracts.py
from dataclasses import dataclass


@dataclass
class GoldTransactionContract:
    email: str
    user_id: int
    user_name: str
    admin_price: float
    admin_weight: float
    transaction_date: str
    transaction_id: int
    weight: float
    price: float
    gold_history_price_base: float
    ref_number: str
    transaction_type: str
    user_from: str
    user_to: str
    transfered_weight: float
    transfered_admin_weight: float
