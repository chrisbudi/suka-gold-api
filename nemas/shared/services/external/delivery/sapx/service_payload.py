from decimal import Decimal

from order.models.order_gold import order_gold
from order.api.serializers.OrderCartSerializer import User
from user.models.users import user, user_address
from core.domain import gold


def generate_submit_payload(
    order: order_gold,
    service_type_code: str,
    gold: gold,
    amount: Decimal,
    user: user,
    user_address: user_address,
    weight: Decimal,
    origin: str,
    destination: str,
):
    payload = {
        "customer_code": user.member_number,
        "reference_no": order.order_gold_id,
        "service_type_code": service_type_code,
        "pickup_place": "1",  # 1 for pickup, 2 for drop-off
        "koli": 1,
        "weight": 1,
        "volumetric": "1x1x1",
        "item_value": float(amount),
        "destination_district_code": "DEV",
        "pickup_name": "Nemas",
        "pickup_address": "",  # nemas address
        "pickup_phone": "",  # nemas phone
        "pickup_email": "",  # nemas email
        "pickup_contact": "",  # nemas contact
        "pickup_district_code": "DEV",  # nemas district code
        "shipment_type_code": "SHTPC",
        "shipment_content_code": "SHTPC",
        "description_item": f"Order {order.order_number} - {gold.brand} {gold.gold_weight} gram",
        "shipper_name": f"",  # nemas name
        "shipper_address": f"",
        "shipper_phone": "",  # nemas phone
        "shipper_contact": f"",  # nemas contact ,
        "receiver_name": f"{user.name}",
        "receiver_address": "{user_address.address}",
        "receiver_phone": "{user_address.phone_number}",
        "receiver_contact": "{user.name}",
    }
    return payload


def generate_price_payload(
    amount: Decimal, weight: Decimal, origin: str, destination: str
):
    payload = {
        "origin": "JK07",
        "destination": "JI28",
        "weight": float(weight),
        "customer_code": "DEV000",
        "volumetric": "1x1x1",
        "insurance_type_code": "INS02",
        "item_value": float(amount),
    }
    return payload
