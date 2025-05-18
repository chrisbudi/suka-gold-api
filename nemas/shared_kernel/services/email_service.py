from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


class EmailService:

    def sendMail(self, mail: Mail):
        sendGridEmail = settings.SENDGRID_EMAIL
        sg = SendGridAPIClient(sendGridEmail["API_KEY"])
        response = sg.send(message=mail)
        # add logger here
        if response.status_code == 202:
            print("Email sent successfully")
        else:
            print("Failed to send email")
        return response.status_code

    def get_email_props(self):
        mail = settings.MAIL
        return {
            "NAMA_PERUSAHAAN": mail["NAMA_PERUSAHAAN"],
            "ALAMAT_PERUSAHAAN": mail["ALAMAT_PERUSAHAAN"],
            "TELP": mail["TELP"],
            "TELP_URL": mail["TELP_URL"],
            "WEBSITE": mail["WEBSITE"],
            "WEBSITE_URL": mail["WEBSITE_URL"],
            "SUPPORT": mail["SUPPORT"],
        }
