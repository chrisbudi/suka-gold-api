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
            print(payload, "payload", self.headers)
            response = requests.post(
                self.base_url + "callback_virtual_accounts",
                headers=self.headers,
                data=payload,
            )

            print(payload, self.headers, response.status_code, "payload")
            if response.status_code not in [200, 201]:
                print(response.json(), "failed response")
                response.raise_for_status()
                return None

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
            print(payload, "payload", self.headers, self.base_url)
            self.headers.pop("api-version", None)
            response = requests.post(
                self.base_url
                + f"callback_virtual_accounts/external_id={reference_id}/simulate_payment",
                headers=self.headers,
                data=payload,
            )
            print(response.json(), "response")
            if response.status_code not in [200, 201]:
                response.raise_for_status()
                return None

            return response.json()
        except Exception as e:
            raise Exception(f"Failed to simulate VA payment : {str(e)}")
