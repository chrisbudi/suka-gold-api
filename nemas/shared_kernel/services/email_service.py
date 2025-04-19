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
