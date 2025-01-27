import requests
from .xendit_services import XenditService


# import xendit service class
class QRISPaymentService(XenditService):

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
            if response.status_code != 200:
                return response.json()

            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to QRIS files : {str(e)}")

    def qris_payment_simulate(self, reference_id: str, payload=None):
        """
        Simulate QRIS payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            response = requests.post(
                self.base_url + f"qr_codes/{reference_id}/payments/simulate",
                headers=self.headers,
                data=payload,
            )

            return response.json()
        except Exception as e:
            raise Exception(f"Failed to simulate QRIS payment : {str(e)}")
