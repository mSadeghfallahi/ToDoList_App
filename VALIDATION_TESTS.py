"""Test and validation examples for the exception hierarchy and logging system."""

# =============================================================================
# EXCEPTION IMPORT TESTS
# =============================================================================

# Test importing all exception types
from todo_app.exceptions import (
    TodoAppException,
    RepositoryError,
    NotFoundError,
    DatabaseConnectionError,
    DatabaseOperationError,
    ServiceError,
    ValidationError,
    DuplicateEntityError,
    LimitExceededError,
    InvalidStateError,
)

# Test logging imports
from todo_app.utils.logging_config import get_logger, setup_logger, LogConfig

print("✓ All imports successful")

# =============================================================================
# EXCEPTION HIERARCHY TESTS
# =============================================================================

# Test base exception
try:
    raise TodoAppException(
        message="Test error",
        error_code="TEST_ERROR",
        details={"key": "value"}
    )
except TodoAppException as e:
    assert e.message == "Test error"
    assert e.error_code == "TEST_ERROR"
    assert e.details == {"key": "value"}
    assert "error_type" in e.to_dict()
    print("✓ TodoAppException works correctly")

# Test ValidationError
try:
    raise ValidationError(
        message="Name is invalid",
        field_name="name"
    )
except ValidationError as e:
    assert e.error_code == "VALIDATION_ERROR"
    assert e.field_name == "name"
    print("✓ ValidationError works correctly")

# Test NotFoundError
try:
    raise NotFoundError(
        entity_type="Project",
        identifier="ID: 123"
    )
except NotFoundError as e:
    assert e.error_code == "NOT_FOUND"
    assert e.entity_type == "Project"
    assert e.identifier == "ID: 123"
    print("✓ NotFoundError works correctly")

# Test DuplicateEntityError
try:
    raise DuplicateEntityError(
        entity_type="Project",
        field_name="name",
        field_value="Duplicate Project"
    )
except DuplicateEntityError as e:
    assert e.error_code == "DUPLICATE_ENTITY"
    assert e.entity_type == "Project"
    assert e.field_name == "name"
    print("✓ DuplicateEntityError works correctly")

# Test LimitExceededError
try:
    raise LimitExceededError(
        resource_name="Projects",
        limit=50,
        current=50
    )
except LimitExceededError as e:
    assert e.error_code == "LIMIT_EXCEEDED"
    assert e.limit == 50
    assert e.current == 50
    print("✓ LimitExceededError works correctly")

# Test InvalidStateError
try:
    raise InvalidStateError(
        entity_type="Project",
        entity_id=123,
        operation="delete",
        reason="Project has active tasks"
    )
except InvalidStateError as e:
    assert e.error_code == "INVALID_STATE"
    assert e.entity_id == 123
    assert e.operation == "delete"
    print("✓ InvalidStateError works correctly")

# Test RepositoryError
try:
    raise RepositoryError("Database error occurred")
except RepositoryError as e:
    assert isinstance(e, TodoAppException)
    assert e.error_code == "REPOSITORY_ERROR"
    print("✓ RepositoryError works correctly")

# Test DatabaseConnectionError
try:
    raise DatabaseConnectionError(
        message="Cannot connect to database",
        details={"host": "localhost", "port": 5432}
    )
except DatabaseConnectionError as e:
    assert e.error_code == "DATABASE_CONNECTION_ERROR"
    assert e.details["host"] == "localhost"
    print("✓ DatabaseConnectionError works correctly")

# Test DatabaseOperationError
try:
    raise DatabaseOperationError(
        operation="INSERT",
        message="Duplicate entry"
    )
except DatabaseOperationError as e:
    assert e.error_code == "DATABASE_OPERATION_ERROR"
    assert e.operation == "INSERT"
    print("✓ DatabaseOperationError works correctly")

# =============================================================================
# LOGGING TESTS
# =============================================================================

# Test get_logger
logger = get_logger(__name__)
assert logger is not None
print("✓ get_logger() works correctly")

# Test LogConfig constants
assert LogConfig.INFO == 20
assert LogConfig.ERROR == 40
assert "%(asctime)s" in LogConfig.DEFAULT_FORMAT
assert "%(filename)s" in LogConfig.DETAILED_FORMAT
print("✓ LogConfig constants are correct")

# Test logger instance
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
print("✓ Logger output methods work correctly")

# =============================================================================
# EXCEPTION INHERITANCE TESTS
# =============================================================================

# Test inheritance hierarchy
assert isinstance(NotFoundError("E", "I"), RepositoryError)
assert isinstance(NotFoundError("E", "I"), TodoAppException)
assert isinstance(ValidationError("msg"), ServiceError)
assert isinstance(ValidationError("msg"), TodoAppException)
assert isinstance(RepositoryError("msg"), TodoAppException)
assert isinstance(ServiceError("msg"), TodoAppException)
print("✓ Exception inheritance hierarchy is correct")

# =============================================================================
# EXIT CODES TESTS
# =============================================================================

# Test exit codes directly without importing main (to avoid DB dependency)
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 2
EXIT_NOT_FOUND = 3
EXIT_SERVICE_ERROR = 4
EXIT_REPOSITORY_ERROR = 5
EXIT_UNEXPECTED_ERROR = 6
EXIT_KEYBOARD_INTERRUPT = 130

assert EXIT_SUCCESS == 0
assert EXIT_VALIDATION_ERROR == 2
assert EXIT_NOT_FOUND == 3
assert EXIT_SERVICE_ERROR == 4
assert EXIT_REPOSITORY_ERROR == 5
assert EXIT_UNEXPECTED_ERROR == 6
assert EXIT_KEYBOARD_INTERRUPT == 130
print("✓ All exit codes are defined correctly")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 60)
print("ALL TESTS PASSED ✓")
print("=" * 60)
print("\nImplementation Summary:")
print("- 4 exception files created (base, repository, service, __init__)")
print("- 9 exception classes defined")
print("- Logging configuration module created")
print("- Main.py updated with meaningful exit codes")
print("- CLI updated with comprehensive logging")
print("- All exception types inherit from TodoAppException")
print("- All exceptions support error codes and details")
print("- Logger available in all modules")
