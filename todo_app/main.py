import sys
import logging
from todo_app.utils.logging_config import setup_logger
from todo_app.utils.deprecation import show_deprecation_notice
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
    # Support a non-interactive subcommand to run background jobs, e.g.
    # `todo tasks:autoclose-overdue` or `todolist tasks:autoclose-overdue`.
    args = sys.argv[1:]
    # Show a deprecation notice for CLI usage (interactive and subcommands)
    show_deprecation_notice('To-Do CLI')
    if args:
        # Only support the specific subcommand for now
        if args[0] == "tasks:autoclose-overdue":
            try:
                # Lazy import of the job implementation
                from todo_app.commands.autoclose_overdue import autoclose_overdue_tasks

                logger.info("Running autoclose_overdue job from CLI")
                closed = autoclose_overdue_tasks()
                logger.info(f"Auto-closed {closed} overdue task(s).")
                print(f"Auto-closed {closed} overdue task(s).")
                return EXIT_SUCCESS
            except RepositoryError as e:
                logger.error(f"Repository error while running autoclose job: {e}", exc_info=True)
                print(f"Error: {e}")
                return EXIT_REPOSITORY_ERROR
            except TodoAppException as e:
                logger.error(f"Application error while running autoclose job: {e}", exc_info=True)
                print(f"Error: {e}")
                return EXIT_SERVICE_ERROR
            except Exception as e:
                logger.critical(f"Unexpected error while running autoclose job: {e}", exc_info=True)
                print(f"Unexpected error: {e}")
                return EXIT_UNEXPECTED_ERROR
        # Unknown subcommand: fall through to interactive or return error
        # We'll print a helpful message and return non-zero
        print(f"Unknown command: {' '.join(args)}")
        return EXIT_UNEXPECTED_ERROR
    try:
        # Import CLI lazily to avoid importing DB-related modules when running non-interactive commands
        from todo_app.cli import TodoCLI

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