from abc import ABC, abstractmethod
from .entities import ContactRequest


class ContactRequestRepository(ABC):
    @abstractmethod
    def save(self, contact_request: ContactRequest):
        pass

    @abstractmethod
    def list_all(self) -> list:
        pass
