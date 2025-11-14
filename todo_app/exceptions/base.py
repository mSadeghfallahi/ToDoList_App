"""Base exception classes for the To-Do List Application."""

from typing import Optional


class TodoAppException(Exception):
    """Base exception class for all application-specific exceptions.
    
    All custom exceptions in the application should inherit from this class
    to allow for unified error handling and logging.
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[dict] = None
    ):
        """Initialize the exception.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code for programmatic handling
            details: Additional context information as a dictionary
        """
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message
    
    def to_dict(self) -> dict:
        """Convert exception to dictionary for logging/API responses.
        
        Returns:
            Dictionary containing error information
        """
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }
