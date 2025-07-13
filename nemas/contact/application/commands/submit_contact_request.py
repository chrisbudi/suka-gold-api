from contact.domain.entities import ContactRequest
from contact.application.services.contact_service import ContactService


class SubmitContactRequestCommand:
    def __init__(self, first_name, last_name, email, phone, message):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.message = message


class SubmitContactRequestHandler:
    def __init__(self, service: ContactService):
        self.service = service

    def handle(self, command):
        return self.service.submit_contact_request(command)
