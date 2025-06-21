import requests
from .xendit_services import XenditService


class DisburstService(XenditService):

    # virtual account payment generate
    def disburst_generate(self, payload=None):
        """
        Generate VA payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            response = requests.post(
                self.base_url + "disbursements",
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

    def disburstment_get(self, reference_id: str, payload=None):
        """
        Simulate VA payment using Xendit API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            response = requests.get(
                self.base_url + f"disbursment/{reference_id}",
                headers=self.headers,
            )
            if response.status_code not in [200, 201]:
                response.raise_for_status()
                return None

            return response.json()
        except Exception as e:
            raise Exception(f"Failed to simulate VA payment : {str(e)}")
