from re import I
from django.conf import settings
import requests
import base64


class XenditService:
    def __init__(self):
        xendit_conf = settings.XENDIT
        self.base_url = xendit_conf["CLIENT_URL"]
        self.headers = {
            "api-version": xendit_conf["API_VERSION"],
            "Content-Type": "application/json",
            "Authorization": f"Basic {(base64.b64encode(xendit_conf["CLIENT_SECRET_KEY"].encode()).decode())}",
        }

    def get_balance(self):
        """
        Get balance from Xendit API.
        :return: Response from the API
        """
        try:
            response = requests.get(
                self.base_url + "balance",
                headers=self.headers,
            )

            return response.json()
        except Exception as e:
            raise Exception(f"Failed to get balance : {str(e)}")

    def get_list_transaction(self):
        """
        Get list of transactions from Xendit API.

        :return: Response from the API
        """
        try:
            response = requests.get(
                self.base_url + "transactions",
                headers=self.headers,
            )

            return response.json()
        except Exception as e:
            raise Exception(f"Failed to get list of transactions : {str(e)}")
