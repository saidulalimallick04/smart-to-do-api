from beanie import Document, Link
from pydantic import Field
from datetime import datetime
from typing import Optional, List
from models.user import User

class Task(Document):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    priority: str = Field(default="medium") # low, medium, high
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    owner: Link[User]

    class Settings:
        name = "tasks"
