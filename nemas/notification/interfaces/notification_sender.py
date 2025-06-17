from abc import ABC, abstractmethod
from typing import Optional


class NotificationSender(ABC):

    @abstractmethod
    def send(self, user, title: str, message: str, data: Optional[dict] = None):
        pass
