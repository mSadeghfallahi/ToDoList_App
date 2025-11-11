"""Abstract repository base class.

Defines the repository contract used across concrete repositories.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Protocol

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):
    """Abstract repository declaring common CRUD operations."""

    @abstractmethod
    def add(self, obj: T) -> T:
        """Add and persist an object to the repository.

        Returns the persisted object (may have primary key populated).
        """

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """Retrieve an object by its primary key."""

    @abstractmethod
    def list(self, **filters) -> List[T]:
        """List objects, optionally filtered by keyword args."""

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete an object by its primary key."""
