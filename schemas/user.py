from pydantic import BaseModel, EmailStr, Field, BeforeValidator, ConfigDict
from typing import Optional, Annotated
from uuid import UUID

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72, description="Password must be between 8 and 72 characters")
    full_name: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: PyObjectId
    email: EmailStr
    full_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
