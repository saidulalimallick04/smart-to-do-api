from beanie import Document, Link
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional, List
from models.user import User

class Task(Document):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    is_completed: bool = False
    priority: str = "medium"
    tags: List[str] = []
    owner: Link[User]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "tasks"
