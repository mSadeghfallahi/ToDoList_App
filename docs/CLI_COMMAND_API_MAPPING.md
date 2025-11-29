# CLI Command → API Endpoint Mapping

This table summarizes how current CLI features map to intended or proposed HTTP API endpoints (Controller). Use it to migrate scripts and user workflows.

| CLI Flow (interactive menu) | Equivalent HTTP Action | Endpoint | Request Body / Query |
|---|---:|---|---|
| `Create Project` | POST | /api/projects | {"name": string, "description": string?}
| `List All Projects` | GET | /api/projects | N/A
| `Edit Project (ID)` | PATCH | /api/projects/{project_id} | {"name"?, "description"?}
| `Delete Project (ID)` | DELETE | /api/projects/{project_id} | N/A
| `Create Task (Project ID)` | POST | /api/projects/{project_id}/tasks | {"title", "description"?, "deadline"?}
| `List Tasks (Project ID)` | GET | /api/projects/{project_id}/tasks | N/A
| `Edit Task (ID)` | PATCH | /api/projects/{project_id}/tasks/{task_id} | {"title"?, "description"?, "deadline"?, "status"?}
| `Delete Task (ID)` | DELETE | /api/projects/{project_id}/tasks/{task_id} | N/A
| `Auto-close Overdue Tasks` | POST | /api/tasks/autoclose | N/A

### Notes:
- Consider adding query parameters for pagination, filtering and sorting (e.g., `?limit=50&offset=0`).
- For `List` endpoints, the API response should include a summary of counts and optionally task previews.
- For safety, add authentication/authorization and rate-limiting at the Controller layer.
