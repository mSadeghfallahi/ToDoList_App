"""Task model for the ToDo application."""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from todo_app.db.base import Base


def utc_now():
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class TaskStatus(enum.Enum):
    """Enumeration for task status."""
    TODO = "to-do"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    CANCELLED = "cancelled"


class Task(Base):
    """
    Task model representing a task in the ToDo application.
    
    Each task belongs to a project and has a status, description, and deadline.
    """
    __tablename__ = "tasks"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Task attributes
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False, index=True)
    deadline = Column(DateTime, nullable=True, index=True)
    
    # Foreign key to Project
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=True)
    
    # Relationship: many-to-one with Project
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f"Task(id={self.id}, name='{self.name}', status='{self.status.value}', project_id={self.project_id})"
    
    def to_dict(self):
        """Convert task to dictionary."""
        return {
            'id': self.id,
            'title': self.name,
            'description': self.description,
            'done': (self.status == TaskStatus.DONE),
            'due_date': self.deadline.isoformat() if self.deadline else None,
            'project_id': self.project_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    # Compatibility / API adapter properties
    @property
    def title(self) -> str:
        return self.name

    @property
    def due_date(self):
        return self.deadline

    @property
    def done(self) -> bool:
        return self.status == TaskStatus.DONE
