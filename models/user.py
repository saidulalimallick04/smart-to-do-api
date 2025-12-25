from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime
from typing import Optional

class User(Document):
    email: EmailStr = Field(unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"
