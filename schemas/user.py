from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    
    class Config:
        from_attributes = True
