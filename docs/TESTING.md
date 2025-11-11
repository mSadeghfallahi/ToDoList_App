# Testing Guide

This guide explains how to test the database setup and models.

## Prerequisites

1. **Docker and Docker Compose** must be installed
2. **PostgreSQL container** must be running
3. **Environment variables** must be configured

## Setup

### 1. Start the PostgreSQL Container

```bash
cd /home/sadegh/Documents/nnn/ToDoList_App
docker-compose -f docker/docker-compose.yml up -d
```

### 2. Create a `.env` File

Create a `.env` file in the project root with the following content:

```env
DB_USER=todo_user
DB_PASSWORD=todo_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todo_db
MAX_NUMBER_OF_PROJECTS=10
```

### 3. Verify Database Connection

Check if the container is running:

```bash
docker-compose -f docker/docker-compose.yml ps
```

## Running Tests

### Option 1: Simple Test Script

Run the simple test script to verify everything works:

```bash
cd /home/sadegh/Documents/nnn/ToDoList_App
poetry run python tests/test_db_setup.py
```

This script will:
- Test database connection
- Create database tables
- Create sample projects and tasks
- Test relationships
- Test query operations

### Option 2: Pytest Tests

Run the comprehensive pytest test suite:

```bash
cd /home/sadegh/Documents/nnn/ToDoList_App
poetry run pytest tests/ -v
```

Run specific test files:

```bash
# Test database connection
poetry run pytest tests/test_db_connection.py -v

# Test models
poetry run pytest tests/test_models.py -v
```

Run with coverage:

```bash
poetry run pytest tests/ --cov=todo_app --cov-report=html
```

## What the Tests Cover

### Database Connection Tests (`test_db_connection.py`)
- Database engine connection
- Table creation
- Session creation
- Base metadata verification

### Model Tests (`test_models.py`)
- **Project Model:**
  - Creating projects
  - Required fields validation
  - to_dict() method
  
- **Task Model:**
  - Creating tasks
  - Required fields validation
  - Status enum values
  - to_dict() method
  
- **Relationships:**
  - Project has many tasks
  - Task belongs to project
  - Cascade delete (deleting project deletes tasks)

## Troubleshooting

### Database Connection Failed

1. Check if Docker container is running:
   ```bash
   docker-compose -f docker/docker-compose.yml ps
   ```

2. Check container logs:
   ```bash
   docker-compose -f docker/docker-compose.yml logs postgres
   ```

3. Verify `.env` file exists and has correct values

### Import Errors

Make sure you're running tests from the project root and using Poetry:

```bash
poetry run pytest tests/
```

### Table Already Exists Errors

If you get errors about tables already existing, you can drop and recreate them:

```python
from todo_app.db.session import engine
from todo_app.db.base import Base

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)
```

## Manual Testing

You can also test interactively using Python:

```python
from todo_app.db.session import SessionLocal, init_db
from todo_app.models import Project, Task, TaskStatus
from datetime import datetime, timedelta

# Initialize database
init_db()

# Create a session
db = SessionLocal()

# Create a project
project = Project(name="My Project", description="Test project")
db.add(project)
db.commit()
db.refresh(project)

# Create a task
task = Task(
    name="My Task",
    description="Test task",
    status=TaskStatus.TODO,
    deadline=datetime.utcnow() + timedelta(days=7),
    project_id=project.id
)
db.add(task)
db.commit()
db.refresh(task)

# Query data
projects = db.query(Project).all()
tasks = db.query(Task).all()

print(f"Projects: {len(projects)}")
print(f"Tasks: {len(tasks)}")

db.close()
```

