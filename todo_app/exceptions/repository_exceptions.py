"""Repository layer exceptions for database and data access operations."""

from typing import Optional
from todo_app.exceptions.base import TodoAppException


class RepositoryError(TodoAppException):
    """Base exception for all repository/data access layer errors.
    
    Raised when there are issues with database operations, data retrieval,
    or persistence operations.
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "REPOSITORY_ERROR",
        details: Optional[dict] = None
    ):
        super().__init__(message, error_code, details)


class NotFoundError(RepositoryError):
    """Exception raised when a requested resource is not found in the database.
    
    This is used when querying for entities that don't exist by ID or other
    unique identifiers.
    
    Examples:
        - Project with ID 123 not found
        - Task with ID 456 not found
        - User with email "test@example.com" not found
    """
    
    def __init__(
        self,
        entity_type: str,
        identifier: str,
        details: Optional[dict] = None
    ):
        """Initialize NotFoundError.
        
        Args:
            entity_type: Type of entity not found (e.g., "Project", "Task")
            identifier: Description of what was searched for (e.g., "ID: 123")
            details: Additional context information
        """
        message = f"{entity_type} not found ({identifier})"
        super().__init__(message, "NOT_FOUND", details)
        self.entity_type = entity_type
        self.identifier = identifier


class DatabaseConnectionError(RepositoryError):
    """Exception raised when database connection fails.
    
    This occurs when the application cannot connect to the database or
    the connection is lost during an operation.
    """
    
    def __init__(
        self,
        message: str = "Failed to connect to database",
        details: Optional[dict] = None
    ):
        super().__init__(message, "DATABASE_CONNECTION_ERROR", details)


class DatabaseOperationError(RepositoryError):
    """Exception raised when a database operation fails.
    
    This includes errors like constraint violations, transaction failures,
    or other database-specific errors.
    """
    
    def __init__(
        self,
        operation: str,
        message: str,
        details: Optional[dict] = None
    ):
        """Initialize DatabaseOperationError.
        
        Args:
            operation: The database operation that failed (e.g., "INSERT", "UPDATE", "DELETE")
            message: Detailed error message from the database
            details: Additional context information
        """
        full_message = f"Database {operation} operation failed: {message}"
        super().__init__(full_message, "DATABASE_OPERATION_ERROR", details)
        self.operation = operation
