# To-Do List Application

A CLI-based To-Do list application with project/task management, auto-close overdue tasks, structured exceptions, and comprehensive logging.

## Quick Setup

**Prerequisites:** Python 3.8+, Poetry, Docker

```bash
# 1. Install dependencies
poetry install

# 2. Create .env file
cat > .env << 'EOF'
DB_USER=todo_user
DB_PASSWORD=todo_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todo_db
MAX_NUMBER_OF_PROJECTS=10
EOF

# 3. Start database
docker-compose up -d

# 4. Run migrations
poetry run alembic -c alembic/alembic.ini upgrade head
```

## Usage

### Interactive CLI
```bash
poetry run todo
# or
poetry run todolist
```

Menu options:
- **Project Management** - Create, edit, delete projects
- **Task Management** - Create, edit, delete, list tasks  
- **List All Projects** - View all projects and task counts

### Background Job - Auto-Close Overdue Tasks
```bash
poetry run todo tasks:autoclose-overdue
```
Closes all tasks with `deadline < now()` and `status != DONE`.

## Features

**Core:**
- Project management (CRUD)
- Task management with status (to-do, in-progress, done, cancelled)
- Deadlines and task descriptions
- Input validation
- Cascade deletion

**Advanced:**
- Auto-close overdue tasks job
- Structured exception hierarchy (9 exception types)
- Centralized logging (console + optional file)
- Meaningful exit codes (0, 2, 3, 4, 5, 6, 130)
- Production-ready with rotating logs

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Validation Error |
| 3 | Not Found |
| 4 | Service Error |
| 5 | Repository/Database Error |
| 6 | Unexpected Error |
| 130 | User Interrupt (Ctrl+C) |

## Testing

```bash
# Run all tests
poetry run pytest tests/ -v

# Run specific test
poetry run pytest tests/test_models.py -v

# With coverage
poetry run pytest tests/ --cov=todo_app --cov-report=html
```

## Project Structure

```
todo_app/
├── cli/              # Interactive menu (console.py)
├── exceptions/       # Exception hierarchy
├── services/         # Business logic
├── models/           # Database models
├── db/               # Database setup
├── utils/            # Validation & logging
├── commands/         # Background jobs
└── main.py           # Entry point
```

## Documentation

- **[docs/EXCEPTIONS_AND_LOGGING.md](docs/EXCEPTIONS_AND_LOGGING.md)** - Exception types & logging setup
- **[docs/TESTING.md](docs/TESTING.md)** - Testing guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Code patterns & examples
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - Full implementation details

## Scheduling Auto-Close Job

### Cron (runs daily at 1 AM)
```bash
0 1 * * * cd /path/to/ToDoList_App && poetry run todo tasks:autoclose-overdue >> /var/log/todo-autoclose.log 2>&1
```

### Systemd Timer (Linux)
See [docs/EXCEPTIONS_AND_LOGGING.md](docs/EXCEPTIONS_AND_LOGGING.md) for systemd service/timer configuration.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: psycopg2` | Run `poetry install` |
| Cannot connect to database | Run `docker-compose up -d` |
| Missing `.env` file | Create it with values from Quick Setup above |

## Common Commands

```bash
# Interactive mode
poetry run todo

# Auto-close job
poetry run todo tasks:autoclose-overdue

# Run tests
poetry run pytest tests/ -v

# Database migrations
poetry run alembic -c alembic/alembic.ini upgrade head
poetry run alembic -c alembic/alembic.ini current
poetry run alembic -c alembic/alembic.ini downgrade -1
```

## Architecture

**Layers:**
- **CLI** (todo_app/cli/) - User interaction
- **Services** (todo_app/services/) - Business logic
- **Repositories** (todo_app/repositories/) - Data access
- **Models** (todo_app/models/) - Database schemas
- **Database** (todo_app/db/) - Connection & session

**Error Handling:**
- 9 exception types organized by layer
- Machine-readable error codes
- Rich error context (message, code, details)

**Logging:**
- Per-module loggers
- 5 log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Console output + optional rotating file handlers
- Structured with timestamps, module names, line numbers
