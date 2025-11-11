# To-Do List Application

A CLI-based To-Do list application with project and task management.

## Installation

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Create .env file:
```bash
cp .env.example .env
```

4. Start the PostgreSQL database:
```bash
docker-compose -f docker/docker-compose.yml up -d
```

5. Run database migrations:
```bash
poetry run alembic -c alembic/alembic.ini upgrade head
```

## Usage

Run the application:
```bash
poetry run todo
```

## Features

- Create, edit, and delete projects
- Create, edit, and delete tasks within projects
- List all projects and tasks
- Task status management (to-do, doing, done)
- Input validation
- Cascade deletion

## Project Structure

```
ToDoList_App/
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore rules
├── pyproject.toml       # Project dependencies and configuration
├── poetry.lock          # Locked dependencies
├── alembic/             # Database migrations
├── docker/              # Docker configuration
├── docs/                # Documentation
├── tests/               # Test files
└── todo_app/            # Application code
```

## Testing

See [TESTING.md](TESTING.md) for detailed testing instructions.

## Database Migrations

See [alembic/README](../alembic/README) for database migration instructions.
