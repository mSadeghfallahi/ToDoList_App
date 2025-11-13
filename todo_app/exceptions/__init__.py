"""Exception hierarchy for the To-Do List Application.

This package defines all custom exceptions used throughout the application,
organized by layer:
- base.py: Base exception classes
- repository_exceptions.py: Data access and database errors
- service_exceptions.py: Business logic and validation errors
"""

from todo_app.exceptions.base import TodoAppException
from todo_app.exceptions.repository_exceptions import (
    RepositoryError,
    NotFoundError,
    DatabaseConnectionError,
    DatabaseOperationError,
)
from todo_app.exceptions.service_exceptions import (
    ServiceError,
    ValidationError,
    DuplicateEntityError,
    LimitExceededError,
    InvalidStateError,
)

__all__ = [
    # Base
    "TodoAppException",
    # Repository exceptions
    "RepositoryError",
    "NotFoundError",
    "DatabaseConnectionError",
    "DatabaseOperationError",
    # Service exceptions
    "ServiceError",
    "ValidationError",
    "DuplicateEntityError",
    "LimitExceededError",
    "InvalidStateError",
]
