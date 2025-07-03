from decimal import Decimal
from user.models.users import user_address


def generate_price_payload(address: user_address, service_name: str) -> dict:
    """Generate payload for Paxel service with service type validation."""

    # Validate service_name
    valid_services = ["SAMEDAY", "NEXTDAY"]
    if service_name not in valid_services:
        raise ValueError(
            f"Invalid service_name: {service_name}. Must be one of {valid_services}"
        )

    # origin address is hardcoded for now, can be changed later
    payload = {
        "origin": {
            "address": "Jl. Sultan Iskandar Muda No.6C",
            "province": "DKI Jakarta",
            "city": "Kota Jakarta Selatan",
            "district": "Kebayoran Lama",
            "village": "Kby. Lama Sel",
            "zip_code": "12210",
            "longitude": float(106.776544),
            "latitude": float(-6.244392),
        },
        "destination": {
            "address": address.address,
            "province": address.province,
            "city": address.city,
            "district": address.district,
            "village": address.subdistrict,
            "zip_code": address.postal_code,
            "longitude": float(address.longtitude),
            "latitude": float(address.latitude),
        },
        "weight": 1000,
        "dimension": "1x1x1",
        "service_type": service_name,  # Use the service_name parameter
    }
    return payload
