# Quick Reference Guide - Exceptions & Logging

## Quick Start

### Import Exceptions
```python
from todo_app.exceptions import (
    ValidationError,
    NotFoundError,
    DuplicateEntityError,
    ServiceError,
    RepositoryError
)
```

### Import Logging
```python
from todo_app.utils.logging_config import get_logger

logger = get_logger(__name__)
```

## Common Exception Patterns

### Validation
```python
from todo_app.exceptions import ValidationError

if not name or not name.strip():
    raise ValidationError(
        message="Name cannot be empty",
        field_name="name"
    )
```

### Not Found
```python
from todo_app.exceptions import NotFoundError

project = db.get(Project, project_id)
if not project:
    raise NotFoundError(
        entity_type="Project",
        identifier=f"ID: {project_id}"
    )
```

### Duplicate Entity
```python
from todo_app.exceptions import DuplicateEntityError

if self._is_name_exists(db, name):
    raise DuplicateEntityError(
        entity_type="Project",
        field_name="name",
        field_value=name
    )
```

### Limit Exceeded
```python
from todo_app.exceptions import LimitExceededError

if len(projects) >= MAX_PROJECTS:
    raise LimitExceededError(
        resource_name="Projects",
        limit=MAX_PROJECTS,
        current=len(projects)
    )
```

### Invalid State
```python
from todo_app.exceptions import InvalidStateError

raise InvalidStateError(
    entity_type="Project",
    entity_id=project_id,
    operation="delete",
    reason="Project has active tasks"
)
```

## Common Logging Patterns

### Operation Start (Debug)
```python
logger.debug(f"Creating project with name: {name}")
```

### Operation Success (Info)
```python
logger.info(f"Project created successfully: {project.name} (ID: {project.id})")
```

### Validation/Recovery Error (Warning)
```python
logger.warning(f"Validation error: {e}")
```

### Unexpected Error (Error)
```python
logger.error(f"Database operation failed: {e}", exc_info=True)
```

### Critical Error (Critical)
```python
logger.critical(f"Application cannot continue: {e}", exc_info=True)
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Validation error |
| 3 | Not found error |
| 4 | Service error |
| 5 | Repository/database error |
| 6 | Unexpected error |
| 130 | User interrupt (Ctrl+C) |

## Exception Hierarchy at a Glance

```
TodoAppException
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

## All Exception Classes

### Repository Layer
- `RepositoryError` - Base repository error
- `NotFoundError` - Resource not found
- `DatabaseConnectionError` - Connection failed
- `DatabaseOperationError` - Query/operation failed

### Service Layer
- `ServiceError` - Base service error
- `ValidationError` - Input validation failed
- `DuplicateEntityError` - Entity already exists
- `LimitExceededError` - Resource limit exceeded
- `InvalidStateError` - Invalid operation for state

## Error Code Reference

Each exception has an `error_code` property for programmatic handling:

- `VALIDATION_ERROR` - ValidationError
- `NOT_FOUND` - NotFoundError
- `DUPLICATE_ENTITY` - DuplicateEntityError
- `LIMIT_EXCEEDED` - LimitExceededError
- `INVALID_STATE` - InvalidStateError
- `REPOSITORY_ERROR` - RepositoryError (base)
- `DATABASE_CONNECTION_ERROR` - DatabaseConnectionError
- `DATABASE_OPERATION_ERROR` - DatabaseOperationError
- `SERVICE_ERROR` - ServiceError (base)

## Accessing Exception Details

```python
try:
    # Some operation
    pass
except ValidationError as e:
    # Get error details
    print(e.message)           # Human-readable message
    print(e.error_code)        # Machine-readable code
    print(e.field_name)        # Specific to ValidationError
    print(e.details)           # Additional context dict
    print(e.to_dict())         # Full error as dictionary
```

## Logging to File

```python
from todo_app.utils.logging_config import setup_logger

# Setup logger with file output
logger = setup_logger(
    name=__name__,
    log_file="logs/app.log",
    detailed_format=True
)

# Now all logs go to console AND file
logger.info("This will be in both console and file")
```

## Tips & Best Practices

1. **Always use specific exception types** - Don't use base `ServiceError` or `RepositoryError` directly
2. **Include context in messages** - Add IDs, values, and operation details
3. **Use error codes for handling** - Check `e.error_code` for specific error types
4. **Log at module level** - Set up logger at module top with `logger = get_logger(__name__)`
5. **Use exc_info=True selectively** - Only for unexpected/critical errors to avoid log spam
6. **Provide details dict** - Include additional context for debugging
7. **Handle exceptions at appropriate layer** - Service catches and handles validation, CLI catches all types

## See Also

- `docs/EXCEPTIONS_AND_LOGGING.md` - Full documentation with examples
- `EXCEPTIONS_LOGGING_SUMMARY.md` - Implementation summary
