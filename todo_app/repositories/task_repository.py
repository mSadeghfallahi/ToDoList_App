"""Task-specific repository implementation using SQLAlchemy."""
from __future__ import annotations

from typing import Optional, List
from sqlalchemy.orm import Session

from .sqlalchemy_repository import SQLAlchemyRepository
from todo_app.models.task import Task


class SQLAlchemyTaskRepository(SQLAlchemyRepository[Task]):
    """Repository for Task model."""

    def __init__(self, session: Session):
        super().__init__(session=session, model_class=Task)

    def list_by_project(self, project_id: int) -> List[Task]:
        """Convenience method to list tasks for a project."""
        return self.list(project_id=project_id)
