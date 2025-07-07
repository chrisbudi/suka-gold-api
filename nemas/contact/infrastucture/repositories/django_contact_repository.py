from contact.domain.repositories import ContactRequestRepository
from contact.domain.entities import ContactRequest
from contact.models import ContactRequestModel


class DjangoContactRequestRepository(ContactRequestRepository):
    def save(self, contact_request: ContactRequest):
        ContactRequestModel.objects.create(
            id=contact_request.id,
            first_name=contact_request.first_name,
            last_name=contact_request.last_name,
            email=contact_request.email,
            phone=contact_request.phone,
            message=contact_request.message,
            created_at=contact_request.created_at,
        )

    def list_all(self) -> list:
        return [
            ContactRequest(
                id=obj.id,
                first_name=obj.first_name,
                last_name=obj.last_name,
                email=obj.email,
                phone=obj.phone,
                message=obj.message,
                created_at=obj.created_at,
            )
            for obj in ContactRequestModel.objects.all().order_by("-created_at")
        ]
