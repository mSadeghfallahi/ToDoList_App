# Exception Hierarchy and Logging Guide

This document explains the exception hierarchy and logging setup for the To-Do List Application.

## Exception Hierarchy

The application uses a layered exception hierarchy to provide clear error handling and categorization:

```
TodoAppException (base)
├── RepositoryError
│   ├── NotFoundError
│   ├── DatabaseConnectionError
│   └── DatabaseOperationError
└── ServiceError
    ├── ValidationError
    ├── DuplicateEntityError
    ├── LimitExceededError
    └── InvalidStateError
```

### Base Exception (`base.py`)

**`TodoAppException`** - Base exception class for all application-specific exceptions.

All custom exceptions inherit from this base class. It provides:
- `message`: Human-readable error message
- `error_code`: Machine-readable error code for programmatic handling
- `details`: Additional context information as a dictionary
- `to_dict()`: Method to convert exception to dictionary for logging/API responses

```python
from todo_app.exceptions import TodoAppException

try:
    # Some operation
    pass
except TodoAppException as e:
    print(f"Error: {e.message}")
    print(f"Code: {e.error_code}")
    print(f"Details: {e.to_dict()}")
```

### Repository Exceptions (`repository_exceptions.py`)

Used for data access and database layer errors.

**`RepositoryError`** - Base exception for all repository errors.

**`NotFoundError`** - Raised when a requested resource is not found.
```python
from todo_app.exceptions import NotFoundError

raise NotFoundError(
    entity_type="Project",
    identifier="ID: 123",
    details={"project_id": 123}
)
```

**`DatabaseConnectionError`** - Raised when database connection fails.
```python
from todo_app.exceptions import DatabaseConnectionError

raise DatabaseConnectionError(
    message="Failed to connect to database",
    details={"host": "localhost", "port": 5432}
)
```

**`DatabaseOperationError`** - Raised when a database operation fails.
```python
from todo_app.exceptions import DatabaseOperationError

raise DatabaseOperationError(
    operation="INSERT",
    message="Duplicate entry for unique constraint",
    details={"constraint": "unique_project_name"}
)
```

### Service Exceptions (`service_exceptions.py`)

Used for business logic and validation errors.

**`ServiceError`** - Base exception for all service layer errors.

**`ValidationError`** - Raised when input validation fails.
```python
from todo_app.exceptions import ValidationError

raise ValidationError(
    message="Project name cannot be empty",
    field_name="name",
    details={"max_length": 100}
)
```

**`DuplicateEntityError`** - Raised when creating a duplicate entity.
```python
from todo_app.exceptions import DuplicateEntityError

raise DuplicateEntityError(
    entity_type="Project",
    field_name="name",
    field_value="My Project",
    details={"existing_id": 42}
)
```

**`LimitExceededError`** - Raised when a resource limit is exceeded.
```python
from todo_app.exceptions import LimitExceededError

raise LimitExceededError(
    resource_name="Projects",
    limit=50,
    current=50,
    details={"user_id": 1}
)
```

**`InvalidStateError`** - Raised when an operation is invalid for the current state.
```python
from todo_app.exceptions import InvalidStateError

raise InvalidStateError(
    entity_type="Project",
    entity_id=123,
    operation="delete",
    reason="Project has active tasks",
    details={"active_task_count": 5}
)
```

## Logging Configuration

The application uses Python's standard `logging` module with a custom configuration.

### Setup Logger

Use `setup_logger()` to configure a logger with console and optional file handlers:

```python
from todo_app.utils.logging_config import setup_logger

# In a module
logger = setup_logger(
    name=__name__,
    level=logging.INFO,
    log_file="logs/app.log",
    detailed_format=True
)
```

### Get Logger

Use `get_logger()` to get an existing logger instance:

```python
from todo_app.utils.logging_config import get_logger

logger = get_logger(__name__)
```

### Logging Best Practices

1. **Import at module level:**
   ```python
   from todo_app.utils.logging_config import get_logger
   
   logger = get_logger(__name__)
   ```

2. **Log levels:**
   - `logger.debug()` - Detailed diagnostic information (development)
   - `logger.info()` - General informational messages (user actions)
   - `logger.warning()` - Warning messages (recoverable errors)
   - `logger.error()` - Error messages (exceptions, failures)
   - `logger.critical()` - Critical errors (application breaking)

3. **Use exc_info for exceptions:**
   ```python
   try:
       # Some operation
       pass
   except ValidationError as e:
       logger.warning(f"Validation error: {e}", exc_info=False)
   except Exception as e:
       logger.error(f"Unexpected error: {e}", exc_info=True)
   ```

4. **Use structured logging with context:**
   ```python
   logger.info(f"Project created: {project.name} (ID: {project.id})")
   logger.debug(f"Editing task {task_id} in project {project_id}")
   ```

## Exit Codes

The CLI uses meaningful exit codes to indicate the type of error that occurred:

- `0 (EXIT_SUCCESS)` - Application exited successfully
- `2 (EXIT_VALIDATION_ERROR)` - Validation error
- `3 (EXIT_NOT_FOUND)` - Resource not found error
- `4 (EXIT_SERVICE_ERROR)` - Service layer error
- `5 (EXIT_REPOSITORY_ERROR)` - Repository/database error
- `6 (EXIT_UNEXPECTED_ERROR)` - Unexpected error
- `130 (EXIT_KEYBOARD_INTERRUPT)` - User interrupted (Ctrl+C)

### Using Exit Codes

Exit codes are automatically handled by the main entry point:

```python
# In main.py
def main():
    try:
        cli = TodoCLI()
        cli.run()
        return EXIT_SUCCESS
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return EXIT_VALIDATION_ERROR
    # ... more exception handlers
```

## Migration Guide

### From Old Code

**Old (utils/validators.py):**
```python
class ValidationError(Exception):
    pass
```

**New (exceptions/service_exceptions.py):**
```python
from todo_app.exceptions import ValidationError

raise ValidationError(
    message="Project name cannot be empty",
    field_name="name"
)
```

### Updating Services

1. Replace imports:
   ```python
   # Old
   from todo_app.utils.validators import ValidationError
   
   # New
   from todo_app.exceptions import ValidationError, NotFoundError
   from todo_app.utils.logging_config import get_logger
   
   logger = get_logger(__name__)
   ```

2. Add logging:
   ```python
   try:
       project = db.get(Project, project_id)
       if not project:
           logger.warning(f"Project {project_id} not found")
           raise NotFoundError(
               entity_type="Project",
               identifier=f"ID: {project_id}"
           )
   except NotFoundError:
       raise
   except Exception as e:
       logger.error(f"Database error: {e}", exc_info=True)
       raise
   ```

## Summary

- Use the exception hierarchy to categorize errors
- Log at appropriate levels with context
- Provide meaningful error messages and error codes
- Use exit codes to indicate failure types
- Centralize logging configuration
