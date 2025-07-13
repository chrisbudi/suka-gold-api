from re import sub
from typing import TYPE_CHECKING

from django.conf import settings
from contact.domain.entities import ContactRequest
from contact.domain.repositories import ContactRequestRepository
from shared.services.email_service import EmailService
from sendgrid.helpers.mail import Mail

if TYPE_CHECKING:
    from contact.application.commands.submit_contact_request import (
        SubmitContactRequestCommand,
    )


class ContactService:
    def __init__(self, repository: ContactRequestRepository):
        self.repository = repository

    def submit_contact_request(self, command):
        """handle email to contact email"""
        import uuid
        from datetime import datetime

        contact_request = ContactRequest(
            id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            first_name=command.first_name,
            last_name=command.last_name,
            phone=command.phone,
            email=command.email,
            message=command.message,
        )

        send_email(contact_request)

        # Optionally, you can trigger an email sending process here
        # For example, using a separate EmailService
        return "email sent successfully"


def send_email(contact: ContactRequest) -> bool:
    """Generate an email message from a template."""
    try:
        subject = "Contact Request from " + contact.first_name + " " + contact.last_name
        message = f""
        "You have received a new contact request:\n\n"
        message += f"Name: {contact.first_name} {contact.last_name}\n"
        message += f"Email: {contact.email}\n"
        message += f"Phone: {contact.phone}\n"
        message += f"Message: {contact.message}\n"
        message += f"Created At: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        ""
        mailService = EmailService()

        sendGridEmail = settings.SENDGRID_EMAIL

        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=["ch.budi9@gmail.com"],
            subject=(subject),
            html_content=message,
        )

        mailService.sendMail(message)

        return True
    except FileNotFoundError as e:
        print("Template file not found:", e)
        return False
    except Exception as e:
        print("Failed to render email template:", e)
        return False
