# Exception Hierarchy and Logging Implementation Summary

## Overview

This document summarizes the comprehensive exception hierarchy and logging system implemented for the To-Do List Application.

## Files Created

### 1. Exception Hierarchy (`/todo_app/exceptions/`)

#### `base.py`
- **`TodoAppException`** - Base exception class for all application-specific exceptions
  - Properties: `message`, `error_code`, `details`
  - Methods: `to_dict()` for converting to dictionary format

#### `repository_exceptions.py`
- **`RepositoryError`** - Base exception for repository/data access errors
- **`NotFoundError`** - When a resource is not found in the database
- **`DatabaseConnectionError`** - When database connection fails
- **`DatabaseOperationError`** - When a database operation fails (INSERT, UPDATE, DELETE)

#### `service_exceptions.py`
- **`ServiceError`** - Base exception for service layer errors
- **`ValidationError`** - When input validation fails
- **`DuplicateEntityError`** - When attempting to create a duplicate entity
- **`LimitExceededError`** - When a resource limit is exceeded
- **`InvalidStateError`** - When an operation is invalid for current state

#### `__init__.py`
- Exports all exception classes for easy importing

### 2. Logging Configuration (`/todo_app/utils/logging_config.py`)

- **`LogConfig`** - Configuration class with log levels and formats
  - `DEFAULT_FORMAT` - Standard log format: `timestamp - logger_name - level - message`
  - `DETAILED_FORMAT` - Extended format with file/line numbers for debugging

- **`setup_logger()`** - Configure logger with console and optional file handlers
  - Supports rotating file handlers (10MB max, 5 backups)
  - Customizable log levels and formats

- **`get_logger()`** - Get existing logger instance

### 3. Updated Files

#### `main.py`
- Added meaningful exit codes:
  - `0` - Success
  - `2` - Validation error
  - `3` - Not found error
  - `4` - Service error
  - `5` - Repository error
  - `6` - Unexpected error
  - `130` - Keyboard interrupt (standard SIGINT)

- Added comprehensive exception handling with logging
- Each exception type is caught separately and logged appropriately

#### `cli/console.py`
- Added logging to all CLI operations
- Uses `get_logger()` to get module logger
- Logs at appropriate levels:
  - `debug()` - For operation start/details
  - `info()` - For successful operations
  - `warning()` - For validation/recoverable errors
  - `error()` - For unexpected errors with full traceback

## Exception Hierarchy Structure

```
TodoAppException (base)
│
├── RepositoryError
│   ├── NotFoundError
│   │   └── Properties: entity_type, identifier
│   ├── DatabaseConnectionError
│   └── DatabaseOperationError
│       └── Properties: operation (INSERT/UPDATE/DELETE)
│
└── ServiceError
    ├── ValidationError
    │   └── Properties: field_name
    ├── DuplicateEntityError
    │   └── Properties: entity_type, field_name, field_value
    ├── LimitExceededError
    │   └── Properties: resource_name, limit, current
    └── InvalidStateError
        └── Properties: entity_type, entity_id, operation, reason
```

## Logging Best Practices Implemented

1. **Logger per module**: Each module uses `get_logger(__name__)` to get its own logger
2. **Appropriate log levels**: Different levels used for different situations
3. **Context in messages**: Include relevant IDs, values, and operation details
4. **Exception information**: Use `exc_info=True` only for unexpected errors
5. **Structured data**: Log dictionaries in error details for programmatic access

## Usage Examples

### Creating a Custom Exception

```python
from todo_app.exceptions import ValidationError, DuplicateEntityError

# Validation error
raise ValidationError(
    message="Project name cannot be empty",
    field_name="name",
    details={"max_length": 100}
)

# Duplicate error
raise DuplicateEntityError(
    entity_type="Project",
    field_name="name",
    field_value="My Project",
    details={"existing_id": 42}
)
```

### Using Logging

```python
from todo_app.utils.logging_config import get_logger
from todo_app.exceptions import NotFoundError

logger = get_logger(__name__)

try:
    project = db.get(Project, project_id)
    if not project:
        logger.warning(f"Project {project_id} not found")
        raise NotFoundError("Project", f"ID: {project_id}")
    logger.info(f"Retrieved project: {project.name}")
except NotFoundError as e:
    logger.error(f"Not found error: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

### CLI Exit Codes

```python
# The main.py automatically returns appropriate exit codes
# based on the exception type that occurred

# Exit successfully
$ python -m todo_app.main
$ echo $?  # Output: 0

# Exit with validation error
$ python -m todo_app.main  # (enter invalid input)
$ echo $?  # Output: 2

# Exit with not found error
$ echo $?  # Output: 3
```

## Benefits

1. **Clear Error Categories** - Exceptions are organized by layer (repository, service)
2. **Standardized Error Handling** - All exceptions inherit from `TodoAppException`
3. **Rich Error Information** - Error codes, details, and context for debugging
4. **Centralized Logging** - Consistent logging across all modules
5. **Meaningful Exit Codes** - CLI exits with codes that indicate failure type
6. **Debugging Support** - Detailed logging format with file/line numbers available
7. **Production Ready** - Rotating file handlers prevent log overflow

## Next Steps

### To migrate existing code:

1. Replace imports in services:
   ```python
   # Old
   from todo_app.utils.validators import ValidationError
   
   # New
   from todo_app.exceptions import ValidationError, NotFoundError
   ```

2. Add logging to all service methods:
   ```python
   from todo_app.utils.logging_config import get_logger
   
   logger = get_logger(__name__)
   
   # In methods
   logger.debug(f"Operation details")
   logger.info(f"Operation successful")
   logger.warning(f"Recoverable error")
   logger.error(f"Unexpected error", exc_info=True)
   ```

3. Update exception raising to use new hierarchy:
   ```python
   # Use specific exception types with error codes
   raise NotFoundError("Project", f"ID: {project_id}")
   ```

## Documentation

See `docs/EXCEPTIONS_AND_LOGGING.md` for comprehensive documentation with examples.
