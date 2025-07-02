import requests

from common.responses import NemasReponses
from .xendit_services import XenditService
from datetime import datetime, timedelta
from uuid import uuid4


class VAPaymentService(XenditService):

    def generate_payload(
        self, amount: float, external_id: str, bank_code: str, user, va_number: str
    ):
        payload = {
            "external_id": f"{external_id}_{str(uuid4())}",
            "bank_code": bank_code,
            "name": user.name,
            "expected_amount": float(amount),
            "expiration_date": (datetime.now() + timedelta(minutes=30)).isoformat(),
            "virtual_account_number": va_number,
            "is_closed": True,
            "is_single_use": True,
        }

        return payload

    # virtual account payment generate
    def va_payment_generate(self, payload=None):
        """
        Generate VA payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            print(payload, "payload", self.headers)
            response = requests.post(
                self.base_url + "callback_virtual_accounts",
                headers=self.headers,
                data=payload,
            )

            if response.status_code not in (200, 201):
                return NemasReponses.failure(
                    message="Failed to generate VA payment",
                    errors=response.json(),
                )
            response.raise_for_status()
            return NemasReponses.success(
                data=response.json(),
                message="VA payment generated successfully",
            )
        except Exception as e:
            raise Exception(f"Failed to VA files : {str(e)}")

    def va_payment_simulate(self, reference_id: str, payload=None):
        """
        Simulate VA payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            print(payload, "payload", self.headers, self.base_url)
            self.headers.pop("api-version", None)
            response = requests.post(
                self.base_url
                + f"callback_virtual_accounts/external_id={reference_id}/simulate_payment",
                headers=self.headers,
                data=payload,
            )
            if response.status_code not in (200, 201):
                return NemasReponses.failure(
                    message="Failed to simulate VA payment",
                    errors=response.json(),
                )
            response.raise_for_status()
            return NemasReponses.success(
                data=response.json(),
                message="VA payment simulated successfully",
            )
        except Exception as e:
            raise Exception(f"Failed to simulate VA payment : {str(e)}")
