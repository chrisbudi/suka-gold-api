from dataclasses import dataclass
from typing import Optional


@dataclass
class NotificationDTO:
    user: object
    title: str
    message: str
    data: Optional[dict] = None
