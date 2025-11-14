"""Service layer exceptions for business logic and validation errors."""

from typing import Optional
from todo_app.exceptions.base import TodoAppException


class ServiceError(TodoAppException):
    """Base exception for all service layer errors.
    
    Raised when there are issues with business logic, operations that violate
    business rules, or service-level failures.
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "SERVICE_ERROR",
        details: Optional[dict] = None
    ):
        super().__init__(message, error_code, details)


class ValidationError(ServiceError):
    """Exception raised when input validation fails.
    
    This includes validation of user input like:
    - Invalid names (empty, too long, etc.)
    - Invalid descriptions
    - Invalid dates or statuses
    - Invalid email formats
    - Constraint violations (e.g., duplicate names)
    """
    
    def __init__(
        self,
        message: str,
        field_name: Optional[str] = None,
        details: Optional[dict] = None
    ):
        """Initialize ValidationError.
        
        Args:
            message: Detailed validation error message
            field_name: Name of the field that failed validation (optional)
            details: Additional context information
        """
        super().__init__(message, "VALIDATION_ERROR", details)
        self.field_name = field_name


class DuplicateEntityError(ServiceError):
    """Exception raised when attempting to create a duplicate entity.
    
    This occurs when trying to create a resource that already exists with
    the same unique constraints (e.g., project with same name).
    """
    
    def __init__(
        self,
        entity_type: str,
        field_name: str,
        field_value: str,
        details: Optional[dict] = None
    ):
        """Initialize DuplicateEntityError.
        
        Args:
            entity_type: Type of entity (e.g., "Project", "Task")
            field_name: Name of the field that caused the duplicate (e.g., "name")
            field_value: The value that caused the duplicate
            details: Additional context information
        """
        message = f"{entity_type} with {field_name} '{field_value}' already exists"
        super().__init__(message, "DUPLICATE_ENTITY", details)
        self.entity_type = entity_type
        self.field_name = field_name
        self.field_value = field_value


class LimitExceededError(ServiceError):
    """Exception raised when a resource limit is exceeded.
    
    Examples:
        - Maximum number of projects reached
        - Maximum number of tasks per project reached
        - Maximum file size exceeded
    """
    
    def __init__(
        self,
        resource_name: str,
        limit: int,
        current: int,
        details: Optional[dict] = None
    ):
        """Initialize LimitExceededError.
        
        Args:
            resource_name: Name of the limited resource (e.g., "Projects")
            limit: Maximum allowed quantity
            current: Current quantity
            details: Additional context information
        """
        message = f"Maximum number of {resource_name} ({limit}) reached. Current: {current}"
        super().__init__(message, "LIMIT_EXCEEDED", details)
        self.resource_name = resource_name
        self.limit = limit
        self.current = current


class InvalidStateError(ServiceError):
    """Exception raised when an operation is invalid for the current state.
    
    Examples:
        - Cannot delete a project with active tasks
        - Cannot transition a task to an invalid status
        - Cannot modify a completed task
    """
    
    def __init__(
        self,
        entity_type: str,
        entity_id: int,
        operation: str,
        reason: str,
        details: Optional[dict] = None
    ):
        """Initialize InvalidStateError.
        
        Args:
            entity_type: Type of entity (e.g., "Project", "Task")
            entity_id: ID of the entity
            operation: The operation being attempted
            reason: Why the operation is invalid for current state
            details: Additional context information
        """
        message = f"Cannot {operation} {entity_type} {entity_id}: {reason}"
        super().__init__(message, "INVALID_STATE", details)
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.operation = operation
        self.reason = reason
