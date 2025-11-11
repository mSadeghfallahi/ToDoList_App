"""Project-specific repository implementation using SQLAlchemy."""
from __future__ import annotations

from typing import Optional, List
from sqlalchemy.orm import Session

from .sqlalchemy_repository import SQLAlchemyRepository
from todo_app.models.project import Project


class SQLAlchemyProjectRepository(SQLAlchemyRepository[Project]):
    """Repository for Project model."""

    def __init__(self, session: Session):
        super().__init__(session=session, model_class=Project)

    def list_with_task_counts(self) -> List[Project]:
        """Return projects - caller can inspect project.tasks for counts.

        Note: This is a small helper; further optimizations (joins) can be
        added later if needed.
        """
        return self.list()
