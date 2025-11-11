"""Project model for the ToDo application."""
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from todo_app.db.base import Base


def utc_now():
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


class Project(Base):
    """
    Project model representing a project in the ToDo application.
    
    A project can have multiple tasks associated with it.
    """
    __tablename__ = "projects"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Project attributes
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=True)
    
    # Relationship: one-to-many with Task
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}')"
    
    def to_dict(self):
        """Convert project to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'task_count': len(self.tasks) if self.tasks else 0
        }
