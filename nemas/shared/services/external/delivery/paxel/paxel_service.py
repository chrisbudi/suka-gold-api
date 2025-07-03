from decimal import Decimal
import json
from django.conf import settings
import requests

from common.responses import ServicesResponse
from common.round_value import round_up_to_100
from user.models.users import user_address
from .service_payload import generate_price_payload


class PaxelService:

    def __init__(self):
        paxel_conf = settings.PAXEL
        self.base_url = paxel_conf["API_URL"]
        self.headers = {
            "Content-Type": "application/json",
            "X-Paxel-API-Key": paxel_conf["API_KEY"],
        }

    def get_price(self, payload=None) -> ServicesResponse:
        """ """
        try:
            response = requests.post(
                self.base_url + "/rates/city",
                headers=self.headers,
                data=payload,
            )
            if response.status_code not in (200, 201):
                return {
                    "success": False,
                    "data": response.json(),
                }
            response_data = response.json()
            return {"success": True, "data": response_data.get("data")}
        except requests.exceptions.HTTPError as http_err:
            return {
                "success": False,
                "data": {
                    "status_code": response.status_code,
                    "message": str(http_err),
                },
            }
        except requests.exceptions.RequestException as req_err:
            return {
                "success": False,
                "data": {
                    "status_code": 500,
                    "message": str(req_err),
                },
            }
        except Exception as e:
            raise Exception(f"Failed to get price: {str(e)}")

    def get_shipping_price(
        self, address: user_address, service_name: str
    ) -> ServicesResponse:
        """Generate payload and get shipping price"""
        # Generate the payload
        payload = generate_price_payload(
            address,
            service_name,
        )

        print(f"Generated payload: {payload}")

        # Convert to JSON string
        payload_data = json.dumps(payload)

        # Get the price using the payload
        shipping_data = self.get_price(payload_data)

        print(f"Shipping data response: {shipping_data}")

        return shipping_data.get("data", {})

    # def _get_shipping_details(
    #     self, service_code: str, order_amount: Decimal, shipping_weight: Decimal
    # ) -> ServicesResponse:
    #     # Get the shipping details based on the provided data

    #     payload = generate_price_payload(
    #         order_amount,
    #         shipping_weight,
    #         "",
    #         "",
    #     )

    #     print(payload, "payload")

    #     payload_data = json.dumps(payload)
    #     shipping_data = self.get_price(payload_data)
    #     print(shipping_data, "shipping_data")
    #     if not shipping_data.get("success"):
    #         return {
    #             "success": False,
    #             "data": shipping_data.get("data"),
    #         }

    #     tracking_service_code = service_code
    #     print(shipping_data.get("data").get("data"), "shipping_data")

    #     services = list(
    #         filter(
    #             lambda s: s.get("service_type_code") == tracking_service_code,
    #             shipping_data.get("data", {}).get("services", []),
    #         )
    #     )

    #     service = next(iter(services), {})
    #     print(service, "service")
    #     if not service:
    #         return {
    #             "success": False,
    #             "data": {
    #                 "message": "Service not found",
    #             },
    #         }
    #     # Extracting the required fields from the service
    #     print(service, "service")
    #     insurance = service.get("insurance_cost")
    #     insurance_round = round_up_to_100(insurance)
    #     insurance_admin = service.get("insurance_admin_cost")
    #     packing = service.get("packing_cost")
    #     cost = service.get("cost")
    #     shipping_total = Decimal(service.get("total_cost") or 0)
    #     shipping_total_rounded = round_up_to_100(shipping_total)

    #     print(
    #         insurance,
    #         insurance_round,
    #         insurance_admin,
    #         packing,
    #         cost,
    #         shipping_total,
    #         shipping_total_rounded,
    #     )
    #     return {
    #         "success": True,
    #         "data": {
    #             "insurance": insurance,
    #             "insurance_round": insurance_round,
    #             "insurance_admin": insurance_admin,
    #             "packing": packing,
    #             "cost": cost,
    #             "shipping_total": shipping_total,
    #             "shipping_total_rounded": shipping_total_rounded,
    #         },
    #     }

    # def submit_order(
    #     self,
    #     order_gold_instance,
    #     user,
    #     shipping_data,
    #     delivery_partner,
    # ):
    #     """Generate Payload for order submission to the external service."""
    #     # Prepare the payload for the order submission

    #     # Submit the tracking information to the external service
    #     # This is a placeholder implementation and should be replaced with actual logic
    #     return {
    #         "success": True,
    #         "data": {
    #             "tracking_number": "123456789",
    #             "status": "Tracking submitted successfully",
    #         },
    #     }
