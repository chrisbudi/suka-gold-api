from dataclasses import dataclass
from typing import Optional


@dataclass
class NotificationDTO:
    user_id: str
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    title: str = ""
    message: str = ""
    data: Optional[dict] = None
