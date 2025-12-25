from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

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
    id: str
    title: str
    description: Optional[str] = None
    is_completed: bool
    priority: str
    tags: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
