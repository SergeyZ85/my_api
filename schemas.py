from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime


    class Config:
        orm_mode = True
