import requests
from .xendit_services import XenditService


class VAPaymentService(XenditService):

    # virtual account payment generate
    def va_payment_generate(self, payload=None):
        """
        Generate VA payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            response = requests.post(
                self.base_url + "callback_virtual_accounts",
                headers=self.headers,
                json=payload,
            )

            return response.json()
        except Exception as e:
            raise Exception(f"Failed to VA files : {str(e)}")

    def va_payment_simulate(self, reference_id: str, payload=None):
        """
        Simulate VA payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            response = requests.post(
                self.base_url + f"callback_virtual_accounts/{reference_id}/simulate",
                headers=self.headers,
                json=payload,
            )

            return response.json()
        except Exception as e:
            raise Exception(f"Failed to simulate VA payment : {str(e)}")
