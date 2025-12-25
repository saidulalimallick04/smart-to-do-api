from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional, List

class User(Document):
    email: Indexed(str, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
