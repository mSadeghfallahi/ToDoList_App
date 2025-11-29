from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class TaskStatus(str, Enum):
    todo = "to-do"
    in_progress = "in-progress"
    done = "done"
    cancelled = "cancelled"


class Pagination(BaseModel):
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)


class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    task_count: Optional[int] = 0

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)
    deadline: Optional[datetime]
    status: Optional[TaskStatus] = TaskStatus.todo


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)
    deadline: Optional[datetime]
    status: Optional[TaskStatus]


class TaskRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: TaskStatus
    deadline: Optional[datetime]
    project_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str = Field(..., regex=r"[^@\s]+@[^@\s]+\.[^@\s]+")
    name: Optional[str]
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str] = Field(None, min_length=8)


class UserRead(BaseModel):
    id: int
    email: str
    name: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
