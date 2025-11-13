import sys
from todo_app.cli import TodoCLI

def main():
    """Entry point for the application"""
    try:
        cli = TodoCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()