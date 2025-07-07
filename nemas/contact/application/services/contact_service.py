from typing import TYPE_CHECKING
from contact.domain.entities import ContactRequest
from contact.domain.repositories import ContactRequestRepository

if TYPE_CHECKING:
    from contact.application.commands.submit_contact_request import (
        SubmitContactRequestCommand,
    )


class ContactService:
    def __init__(self, repository: ContactRequestRepository):
        self.repository = repository

    def submit_contact_request(self, command):

        contact = ContactRequest.create(
            command.first_name,
            command.last_name,
            command.email,
            command.phone,
            command.message,
        )
        self.repository.save(contact)
        return contact
