# To-Do API (OpenAPI-style) — /api/v1

This document describes endpoints for LITS (Lists) and Tasks. Lists are equivalent to Projects in the current codebase.

Version prefix: `/api/v1/`

Common query parameters for listing endpoints:
- limit: integer (default 10, max 100) — page size
- offset: integer (default 0) — page offset
- q: string — full-text search across name/title/description
- sort: string (e.g., "created_at", "-created_at", "deadline", "-deadline")
- status: string (for tasks only) — one of: `to-do`, `in-progress`, `done`, `cancelled`
- due_before/due_after: ISO 8601 date/datetime strings for filtering by deadline

Response metadata:
- For list endpoints, include `X-Total-Count` header and optionally `Link` header for paging.

-----------------------------------------
## Resources

### List (Project)

Model (ProjectRead)
```json
{
  "id": 1,
  "name": "Inbox",
  "description": "Personal tasks",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-10T12:35:00Z",
  "task_count": 12
}
```

Endpoints:

- GET /api/v1/lists
  - Query: q, limit, offset, sort, include_tasks (bool)
  - Response: 200 OK, JSON array of ProjectRead
  - Status codes: 200, 400, 500

- POST /api/v1/lists
  - Body: ProjectCreate (name, description?)
  - Response: 201 Created, Location: /api/v1/lists/{id}
  - Status codes: 201, 400, 409, 500

- GET /api/v1/lists/{list_id}
  - Response: 200 OK (ProjectRead) or 404 Not Found
  - Status codes: 200, 404, 500

- PATCH /api/v1/lists/{list_id}
  - Body: ProjectUpdate (name?, description?)
  - Response: 200 OK (ProjectRead)
  - Status codes: 200, 400, 404, 409

- DELETE /api/v1/lists/{list_id}
  - Response: 204 No Content
  - Status codes: 204, 404, 400

-----------------------------------------
### Task

Model (TaskRead)
```json
{
  "id": 123,
  "name": "Buy milk",
  "description": "Remember to get semi-skimmed",
  "status": "to-do",
  "deadline": "2025-12-31T23:59:00Z",
  "project_id": 1,
  "created_at": "2025-12-12T04:12:00Z",
  "updated_at": "2025-12-12T05:22:00Z"
}
```

Endpoints:

- GET /api/v1/tasks
  - Query: q, status, due_before, due_after, limit, offset, sort, project_id(optional)
  - Response: 200 OK, JSON array of TaskRead
  - Status codes: 200, 400, 500

- GET /api/v1/lists/{list_id}/tasks
  - Query: q, status, due_before, due_after, limit, offset, sort
  - Response: 200 OK, JSON array of TaskRead
  - Status codes: 200, 400, 404, 500

- POST /api/v1/lists/{list_id}/tasks
  - Body: TaskCreate
  - Response: 201 Created, Location: /api/v1/lists/{list_id}/tasks/{task_id}
  - Status codes: 201, 400, 404

- GET /api/v1/lists/{list_id}/tasks/{task_id}
  - Response: 200 OK, TaskRead or 404
  - Status codes: 200, 404

- PATCH /api/v1/lists/{list_id}/tasks/{task_id}
  - Body: TaskUpdate
  - Response: 200 OK, TaskRead
  - Status codes: 200, 400, 404

- DELETE /api/v1/lists/{list_id}/tasks/{task_id}
  - Response: 204 No Content
  - Status codes: 204, 404

- POST /api/v1/tasks/autoclose
  - Triggers an auto-close routine for overdue tasks.
  - Response: 200 OK { "closed": n }
  - Status codes: 200, 403, 500

-----------------------------------------
### Authentication & Authorization (notes)
- All write operations should require authentication (e.g., API key or JWT). For the skeleton we mark write endpoints but leave policy integration to implementers.
- For multi-user environments, enforce ownership/scoping (users can only modify tasks they own or lists they belong to).

-----------------------------------------
### Error model (common)
```json
{
  "error_type": "ValidationError",
  "error_code": "VALIDATION_ERROR",
  "message": "Validation failed for field 'name'",
  "details": {}
}
```

Status code mapping (recommended)
- 200 OK - for GET and successful operations returning data.
- 201 Created - for successful resource creation. Include `Location` header.
- 204 No Content - for successful delete no-body responses.
- 400 Bad Request - invalid input or bad query param.
- 401 Unauthorized - authentication required (not authenticated).
- 403 Forbidden - authenticated but not authorized to perform action.
- 404 Not Found - resource not found.
- 409 Conflict - duplicate or conflicting state.
- 422 Unprocessable Entity - RFC validation errors from FastAPI (optional).
- 500 Internal Server Error - unexpected error.
