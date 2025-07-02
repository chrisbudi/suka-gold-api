import requests

from common.responses import NemasReponses
from .xendit_services import XenditService
from uuid import uuid4
from datetime import datetime, timedelta


# import xendit service class
class QRISPaymentService(XenditService):

    def __init__(self):
        super().__init__()

    def generate_payload(self, amount: float, external_id: str):
        payload = {
            "reference_id": f"{external_id}_{str(uuid4())}",
            "type": "DYNAMIC",
            "currency": "IDR",
            "amount": float(amount),
            "expired_at": (datetime.now() + timedelta(hours=2)).strftime("%d/%m/%Y"),
            "channel_code": "ID_DANA",
            "is_closed": True,
        }

        return payload

    def qris_payment_generate(self, payload=None):
        """
        Generate QRIS payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            response = requests.post(
                self.base_url + "qr_codes",
                headers=self.headers,
                data=payload,
            )

            # check if response is not 200
            if response.status_code not in (200, 201):
                return NemasReponses.failure(
                    message="Failed to generate QRIS payment",
                    errors=response.json(),
                )
            response.raise_for_status()
            return NemasReponses.success(
                data=response.json(),
                message="QRIS payment generated successfully",
            )
        except requests.exceptions.HTTPError as http_err:
            return NemasReponses.failure(
                message="Failed to generate QRIS payment",
                errors={"error": str(http_err)},
            )
        except Exception as e:
            raise Exception(f"Failed to generate QRIS payment : {str(e)}")

    def qris_payment_simulate(self, reference_id: str, payload=None):
        """
        Simulate QRIS payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            self.headers.pop("api-version", None)
            print(self.base_url + f"qr_codes/{reference_id}/payments/simulate", "url")
            response = requests.post(
                self.base_url + f"qr_codes/{reference_id}/payments/simulate",
                headers=self.headers,
                data=payload,
            )

            if response.status_code not in (200, 201):
                return NemasReponses.failure(
                    message="Failed to simulate QRIS payment",
                    errors=response.json(),
                )
            response.raise_for_status()
            return NemasReponses.success(
                data=response.json(),
                message="QRIS payment simulated successfully",
            )
        except Exception as e:
            raise Exception(f"Failed to simulate QRIS payment : {str(e)}")
