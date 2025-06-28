from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from ..models.task import TaskStatus

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None

class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class TaskWithUser(TaskResponse):
    creator: "UserResponse"

# Resolve forward references
from .user import UserResponse
TaskWithUser.model_rebuild()