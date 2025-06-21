from django.conf import settings
import requests


class VerihubService:
    def __init__(self):
        veri_conf = settings.VERIHUB
        self.base_url = veri_conf["CLIENT_URL"]
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": veri_conf["CLIENT_TOKEN"],
            "App-ID": veri_conf["APP_ID"],
            "API-Key": veri_conf["API_KEY"],
        }

    def verify_ktp_file(self, payload=None):
        """
        Verify KTP file using Verihub API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            response = requests.post(
                self.base_url + settings.VERIHUB["KTP_SYNC"],
                headers=self.headers,
                json=payload,
            )
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to verify KTP file: {str(e)}")

    def compare_photo_file(self, payload=None):
        """
        Compare photo file using Verihub API.

        :param payload: Payload to send to the API
        :return: Response from the API
        """
        try:
            response = requests.post(
                self.base_url + settings.VERIHUB["COMPARE_PHOTO"],
                headers=self.headers,
                json=payload,
            )
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to compare photo file: {str(e)}")

    def verify_identity(self, payload=None):
        """ """
        try:
            response = requests.post(
                self.base_url + settings.VERIHUB["DATA_VERIFICATION"],
                headers=self.headers,
                json=payload,
            )
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to compare photo file: {str(e)}")
