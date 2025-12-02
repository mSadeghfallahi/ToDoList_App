"""Task repository implementations.

Provides abstract and concrete repositories for managing Task entities.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from todo_app.models.task import Task, TaskStatus
from .sqlalchemy_repository import SQLAlchemyRepository


class TaskDTO:
    """Data Transfer Object for Task creation/updates."""
    
    def __init__(
        self,
        name: str,
        project_id: int,
        description: Optional[str] = None,
        status: str = TaskStatus.TODO.value,
        deadline: Optional[datetime] = None,
        done: Optional[bool] = False,
        due_date: Optional[datetime] = None,
    ):
        self.name = name
        self.project_id = project_id
        self.description = description
        self.status = status
        self.deadline = deadline
        self.done = done
        self.due_date = due_date


class TaskRepository(ABC):
    """Abstract base class defining the contract for task repositories."""

    @abstractmethod
    def create(self, task_dto: TaskDTO) -> Task:
        """Create and persist a new task.
        
        Args:
            task_dto: TaskDTO containing task data
            
        Returns:
            The persisted Task object with populated id
        """

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Task]:
        """Retrieve a task by its primary key.
        
        Args:
            id: Task primary key
            
        Returns:
            Task object or None if not found
        """

    @abstractmethod
    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Task]:
        """List tasks, optionally filtered.
        
        Args:
            filters: Dictionary of field names to filter values
            
        Returns:
            List of matching Task objects
        """

    @abstractmethod
    def update(self, id: int, fields: Dict[str, Any]) -> Optional[Task]:
        """Update a task with new field values.
        
        Args:
            id: Task primary key
            fields: Dictionary of field names to new values
            
        Returns:
            Updated Task object or None if task not found
        """

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete a task by its primary key.
        
        Args:
            id: Task primary key
            
        Returns:
            True if task was deleted, False if not found
        """

    @abstractmethod
    def list_overdue(self, now: datetime) -> List[Task]:
        """List all tasks with deadline before the given datetime.
        
        Args:
            now: Reference datetime for comparison
            
        Returns:
            List of overdue Task objects
        """

    @abstractmethod
    def mark_closed(self, id: int, closed_at: datetime) -> Optional[Task]:
        """Mark a task as closed with the given timestamp.
        
        Updates the task's status to DONE and sets updated_at.
        
        Args:
            id: Task primary key
            closed_at: Datetime when task was closed
            
        Returns:
            Updated Task object or None if not found
        """


class InMemoryTaskRepository(TaskRepository):
    """In-memory implementation storing tasks in a dictionary."""

    def __init__(self):
        """Initialize the in-memory repository."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create(self, task_dto: TaskDTO) -> Task:
        """Create and store a task in memory."""
        task = Task(
            id=self._next_id,
            name=task_dto.name,
            project_id=task_dto.project_id,
            description=task_dto.description,
            status=TaskStatus(task_dto.status),
            deadline=task_dto.deadline,
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_by_id(self, id: int) -> Optional[Task]:
        """Retrieve a task from memory by id."""
        return self._tasks.get(id)

    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Task]:
        """List all tasks, optionally filtered by attributes."""
        tasks = list(self._tasks.values())
        
        if not filters:
            return tasks
        
        # Filter tasks based on provided criteria
        for key, value in filters.items():
            tasks = [
                t for t in tasks
                if getattr(t, key, None) == value
            ]
        
        return tasks

    def update(self, id: int, fields: Dict[str, Any]) -> Optional[Task]:
        """Update a task with new field values."""
        task = self._tasks.get(id)
        if task is None:
            return None
        
        for key, value in fields.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        return task

    def delete(self, id: int) -> bool:
        """Delete a task from memory."""
        if id in self._tasks:
            del self._tasks[id]
            return True
        return False

    def list_overdue(self, now: datetime) -> List[Task]:
        """List tasks with deadline before the given datetime."""
        return [
            task for task in self._tasks.values()
            if task.deadline and task.deadline < now
        ]

    def mark_closed(self, id: int, closed_at: datetime) -> Optional[Task]:
        """Mark a task as DONE and update its timestamp."""
        task = self._tasks.get(id)
        if task is None:
            return None
        
        task.status = TaskStatus.DONE
        task.updated_at = closed_at
        return task


class SqlAlchemyTaskRepository(TaskRepository, SQLAlchemyRepository[Task]):
    """SQLAlchemy-based repository for Task model with session injection."""

    def __init__(self, session: Session):
        """Initialize with an injected SQLAlchemy session.
        
        Args:
            session: SQLAlchemy Session instance for database operations
        """
        super().__init__(session=session, model_class=Task)

    def create(self, task_dto: TaskDTO) -> Task:
        """Create and persist a task to the database."""
        # Map done flag or status string to Task.status enum
        status_val = task_dto.status
        if task_dto.done:
            status_val = TaskStatus.DONE.value
        deadline = task_dto.due_date if task_dto.due_date else task_dto.deadline
        task = Task(
            name=task_dto.name,
            project_id=task_dto.project_id,
            description=task_dto.description,
            status=TaskStatus(status_val),
            deadline=deadline,
        )
        return self.add(task)

    def get_by_id(self, id: int) -> Optional[Task]:
        """Retrieve a task from the database by id."""
        return self.get(id)

    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Task]:
        """List tasks from the database, optionally filtered."""
        if filters is None:
            filters = {}
        return super().list(**filters)

    def update(self, id: int, fields: Dict[str, Any]) -> Optional[Task]:
        """Update a task in the database."""
        task = self.get_by_id(id)
        if task is None:
            return None
        
        for key, value in fields.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, id: int) -> bool:
        """Delete a task from the database."""
        super().delete(id)
        return True

    def list_overdue(self, now: datetime) -> List[Task]:
        """List all tasks with deadline before the given datetime."""
        return self.session.query(Task).filter(
            Task.deadline < now
        ).all()

    def mark_closed(self, id: int, closed_at: datetime) -> Optional[Task]:
        """Mark a task as DONE in the database."""
        task = self.get_by_id(id)
        if task is None:
            return None
        
        task.status = TaskStatus.DONE
        task.updated_at = closed_at
        self.session.commit()
        self.session.refresh(task)
        return task
