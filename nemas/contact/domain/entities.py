from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime


@dataclass
class ContactRequest:
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    message: str
    created_at: datetime

    @staticmethod
    def create(first_name, last_name, email, phone, message):
        return ContactRequest(
            id=str(uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message,
            created_at=datetime.utcnow(),
        )
