from decimal import Decimal
from django.conf import settings
import requests


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
            if response.status_code != 200:
                return {
                    "status": "failed",
                    "message": response.json(),
                }
            response_data = response.json()
            return response_data
        except Exception as e:
            raise Exception(f"Failed to get price: {str(e)}")
