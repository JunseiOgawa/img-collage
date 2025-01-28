from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    image_path: Optional[str] = None

    class Config:
        from_attributes = True
