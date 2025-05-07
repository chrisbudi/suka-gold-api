# contracts.py
from dataclasses import dataclass


@dataclass
class GoldChartDailyContract:
    hour: str
    gold_price_sell: float
    gold_price_buy: float


@dataclass
class GoldChartWeeklyContract:
    day: str
    gold_price_buy: float
    gold_price_sell: float
    timestamps: str
