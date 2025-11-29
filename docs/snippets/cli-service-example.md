# CLI to Service Layer Snippet (Before -> After)

This snippet shows how **CLI code should call the Service layer** instead of creating DB sessions directly. The Service layer is the entry point for business logic and validation. Controllers and API endpoints call the Services; CLI should call services as well.

## Before: CLI (direct DB access)

```python
from todo_app.db.session import SessionLocal
from todo_app.models.project import Project

def create_project_cli_direct(name, description=None):
    db = SessionLocal()
    try:
        project = Project(name=name, description=description)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    finally:
        db.close()
```

This approach ties CLI to DB implementation and is harder to test, reuse, and secure.

## After: CLI (call Service layer)

```python
from todo_app.services.project_manager import ProjectManager

project_service = ProjectManager()

def create_project_cli_service(name, description=None):
    project = project_service.create_project(name, description)
    return project
```

Benefits of this approach:
- Reuses existing business validation and logic
- Simplifies Controller -> Service -> Repository movement when migrating to an API
- Improves testability
- Easier to add permission checks, rate-limiting and authentication at Controller/Layer above Service
