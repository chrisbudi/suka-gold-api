from decimal import Decimal
from typing import TypedDict


class ShippingDetails(TypedDict):

    insurance: Decimal
    insurance_round: Decimal
    insurance_admin: Decimal
    packing: Decimal
    cost: Decimal
    shipping_total: Decimal
    shipping_total_rounded: Decimal
