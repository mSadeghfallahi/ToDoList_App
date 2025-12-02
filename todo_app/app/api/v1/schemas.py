from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import timezone
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
    due_date: Optional[datetime]
    done: Optional[bool] = Field(False)

    @staticmethod
    def _ensure_tz(v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    @staticmethod
    def _validate_due_date(v: Optional[datetime]) -> Optional[datetime]:
        # Allow None
        if v is None:
            return None
        # Accept naive datetimes by assuming UTC - optional
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        return v

    @validator("due_date")
    def due_date_must_be_valid(cls, v: Optional[datetime]):
        return cls._validate_due_date(v)

    @validator("title")
    def title_must_not_be_blank(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("title must not be blank")
        return s


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)
    due_date: Optional[datetime]
    done: Optional[bool]

    @validator("due_date")
    def due_date_must_be_valid(cls, v: Optional[datetime]):
        if v is None:
            return None
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        return v

    @validator("title")
    def title_must_not_be_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        s = v.strip()
        if not s:
            raise ValueError("title must not be blank")
        return s


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    due_date: Optional[datetime]
    project_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# Alias for TaskRead as TaskOut for API user expectations
class TaskOut(TaskRead):
    pass

    # Add validators? Not necessary for read schema, but we can add useful alias if needed


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
