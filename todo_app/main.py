import sys
import logging
from todo_app.cli import TodoCLI
from todo_app.utils.logging_config import setup_logger
from todo_app.exceptions import (
    TodoAppException,
    ValidationError,
    NotFoundError,
    ServiceError,
    RepositoryError
)

# Setup logger for main module
logger = setup_logger(__name__)

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 2
EXIT_NOT_FOUND = 3
EXIT_SERVICE_ERROR = 4
EXIT_REPOSITORY_ERROR = 5
EXIT_UNEXPECTED_ERROR = 6
EXIT_KEYBOARD_INTERRUPT = 130  # Standard SIGINT exit code


def main():
    """Entry point for the application"""
    try:
        cli = TodoCLI()
        cli.run()
        logger.info("Application exited successfully")
        return EXIT_SUCCESS
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}", exc_info=False)
        print(f"\n❌ Validation Error: {e}")
        return EXIT_VALIDATION_ERROR
        
    except NotFoundError as e:
        logger.error(f"Resource not found: {e}", exc_info=False)
        print(f"\n❌ Not Found: {e}")
        return EXIT_NOT_FOUND
        
    except ServiceError as e:
        logger.error(f"Service error: {e}", exc_info=True)
        print(f"\n❌ Service Error: {e}")
        return EXIT_SERVICE_ERROR
        
    except RepositoryError as e:
        logger.error(f"Repository error: {e}", exc_info=True)
        print(f"\n❌ Data Access Error: {e}")
        return EXIT_REPOSITORY_ERROR
        
    except KeyboardInterrupt:
        logger.warning("Application interrupted by user (Ctrl+C)")
        print("\n\nApplication interrupted. Goodbye!")
        return EXIT_KEYBOARD_INTERRUPT
        
    except TodoAppException as e:
        logger.critical(f"Application exception: {e}", exc_info=True)
        print(f"\n❌ Application Error: {e}")
        return EXIT_UNEXPECTED_ERROR
        
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ An unexpected error occurred: {e}")
        return EXIT_UNEXPECTED_ERROR
    
    finally:
        logger.debug("Application cleanup")


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)