from decimal import Decimal
import json
from django.conf import settings
import requests

from common.responses import NemasReponses


class SapxService:

    def __init__(self):
        sapx_conf = settings.SAPX
        self.base_url = sapx_conf["API_URL"]
        self.headers = {
            "Content-Type": "application/json",
            "API_Key": sapx_conf["API_KEY"],
        }

    def generate_payload(
        self, amount: Decimal, weight: Decimal, origin: str, destination: str
    ):
        payload = {
            "origin": "JK07",
            "destination": "JI28",
            "weight": float(weight),
            "customer_code": "DEV000",
            "packing_type_code": "ACH06",
            "volumetric": "1x1x1",
            "insurance_type_code": "INS02",
            "item_value": float(amount),
        }
        return payload

    def get_district(self, payload=None):
        """ """
        try:
            response = requests.get(
                self.base_url + "v2/master/district/get",
                headers=self.headers,
            )
            response_data = response.json()
            return response_data.get("data", [])
        except Exception as e:
            raise Exception(f"Failed to verify KTP file: {str(e)}")

    def get_shipping_content(self, payload=None):
        """ """
        try:
            response = requests.get(
                self.base_url + "v2/master/shipment_content/get",
                headers=self.headers,
            )
            response_data = response.json()

            print(response_data, "response_data")
            return response_data.get("data", [])
        except Exception as e:
            raise Exception(f"Failed to get data: {str(e)}")

    def get_price(self, payload=None):
        """ """
        try:
            response = requests.post(
                self.base_url + "v2/master/shipment_cost",
                headers=self.headers,
                data=payload,
            )
            if response.status_code not in (200, 201):
                return NemasReponses.failure(
                    message="Failed to get price",
                    errors=response.json(),
                )
            response_data = response.json()
            return NemasReponses.success(
                data=response_data.get("data", []),
                message="Price retrieved successfully",
            )
        except requests.exceptions.HTTPError as http_err:
            return NemasReponses.failure(
                message="Failed to get price",
                errors={"error": str(http_err)},
            )
        except requests.exceptions.RequestException as req_err:
            return NemasReponses.failure(
                message="Failed to get price",
                errors={"error": str(req_err)},
            )
        except Exception as e:
            raise Exception(f"Failed to get price: {str(e)}")

    def _get_shipping_details(
        self, service_code: str, order_amount: Decimal, shipping_weight: Decimal
    ):
        # Get the shipping details based on the provided data

        payload = self.generate_payload(
            order_amount,
            shipping_weight,
            "",
            "",
        )
        payload_data = json.dumps(payload)

        shipping_data = self.get_price(payload_data)
        if not shipping_data.get("success"):
            return NemasReponses.failure(
                message="Failed to get price",
                errors={"error": shipping_data.get("message")},
            )

        # tracking_service_code = validated_data.get("tracking_courier_service_code")
        tracking_service_code = service_code
        services = list(
            filter(
                lambda s: s.get("service_type_code") == tracking_service_code,
                shipping_data["data"].get("data", {}).get("services", []),
            )
        )
        service = next(iter(services), {})

        insurance = service.get("insurance")
        insurance_round = (insurance // 100 * 100 + 100) if insurance is not None else 0
        insurance_admin = service.get("insurance_admin")
        packing = service.get("packing")
        cost = service.get("cost")
        shipping_total = Decimal(service.get("total") or 0)
        shipping_total_rounded = shipping_total // 100 * 100 + 100

        return {
            "insurance": insurance,
            "insurance_round": insurance_round,
            "insurance_admin": insurance_admin,
            "packing": packing,
            "cost": cost,
            "shipping_total": shipping_total,
            "shipping_total_rounded": shipping_total_rounded,
        }
