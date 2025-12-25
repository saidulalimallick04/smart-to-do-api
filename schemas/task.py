from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Optional, List, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    tags: List[str] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None

class TaskOut(BaseModel):
    id: PyObjectId
    title: str
    description: Optional[str] = None
    is_completed: bool
    priority: str
    tags: List[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
