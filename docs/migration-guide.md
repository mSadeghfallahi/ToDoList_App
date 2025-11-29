# Migration Guide: Move from CLI to API

This guide outlines how to migrate your workflows from the CLI to the HTTP API (Controller → Service → Repository). The CLI is now deprecated and will be removed in a future release; headers and logs warn users that migration is required.

## Overview

- Deprecation: The `todo` CLI is deprecated; begin migrating now.
- Migration target: HTTP REST API endpoints (Controller layer) that call into Service → Repository stacks.
- Deadline: See `Config.CLI_DEPRECATION_DATE` (default `2026-01-01`) and the project README.

## Migration Steps

1. Add an HTTP Controller layer (for example using FastAPI or Flask) with endpoints that call the existing Service layer.
2. Ensure Services (e.g., `ProjectManager`, `TaskManager`) are thread-safe or adapted to the request lifecycle.
3. For background tasks (autoclose-overdue), create an API endpoint/triggers + a CRON/systemd timer that calls the endpoint.
4. Replace CLI-based invocations in deployment scripts with API calls (curl, HTTP clients) or a REST client library.
5. Update documentation, integration tests, and CI to target API endpoints.
6. Start rolling out and migrate users to the API; deprecate the CLI per the migration timeline.

## Mapping Table (CLI Command → API Endpoint)

| CLI Action | HTTP Method | Endpoint | Body/Query | Description |
|---|---:|---|---|---|
| Create Project | POST | /api/projects | { name, description? } | Create a new project |
| List Projects | GET | /api/projects | N/A | List all projects with task counts |
| Edit Project | PATCH | /api/projects/{project_id} | { name?, description? } | Update name or description |
| Delete Project | DELETE | /api/projects/{project_id} | N/A | Delete a project (cascade deletes tasks) |
| Create Task | POST | /api/projects/{project_id}/tasks | { title, description?, status?, deadline } | Create a task in a project |
| List Tasks | GET | /api/projects/{project_id}/tasks | N/A | List tasks in a project |
| Edit Task | PATCH | /api/projects/{project_id}/tasks/{task_id} | { title?, description?, status?, deadline? } | Update a task |
| Delete Task | DELETE | /api/projects/{project_id}/tasks/{task_id} | N/A | Delete a task |
| Auto-Close Overdue Tasks | POST | /api/tasks/autoclose | N/A | Run the overdue closure routine |

> Tip: Design your endpoints following RESTful practices and use HTTP status codes (2xx, 4xx, 5xx) consistent with current exit codes.

## Example API Call (curl)

Create a project:

```bash
curl -s -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Inbox", "description": "Personal tasks"}'
```

Create task:

```bash
curl -s -X POST http://localhost:8000/api/projects/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "deadline": "2025-12-31"}'
```

## Implementation Notes

- Keep Services untouched and call them from your Controllers to reuse existing business logic and validation.
- Controllers translate HTTP input into Service calls and map exceptions to appropriate HTTP codes.
- Add a small adaptor to translate request-scoped DB sessions into the existing SessionLocal pattern.

## Quick Code Example (FastAPI controller)

```python
from fastapi import FastAPI, HTTPException
from todo_app.services.project_manager import ProjectManager
from todo_app.exceptions import ValidationError

app = FastAPI()
project_service = ProjectManager()

@app.post('/api/projects')
def create_project(body: dict):
    try:
        project = project_service.create_project(body['name'], body.get('description'))
        return project.__dict__
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Rollout & Announcement

1. Create an announcement changelog on README and release notes.
2. Run a Beta where both CLI and API are available, and monitor usage. Add analytics support to measure CLI use vs API.
3. Encourage API adoption by providing migration snippets and examples.

## Reverting if needed

If the API reveals critical bugs, the release manager can toggle the CLI back or extend the deprecation timeline. Use `DISABLE_CLI_DEPRECATION_WARNING=true` to hide the messages temporarily.
