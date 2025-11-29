# API Routes — /api/v1

This document defines the routes and examples for the To-Do project API. Follow RESTful naming, use plural resources, and version the API under `/api/v1/`.

## Global query parameters and pagination
- `limit` (int, default 10, max 100) — number of items to return
- `offset` (int, default 0) — number of items to skip
- `q` (string) — free-text search across `name`, `title`, `description`
- `sort` (string) — sort field (e.g., `created_at`, `deadline`)
- Always provide `Link` or `X-Total-Count` headers when serving lists for clients to know total counts and next offsets.

## Projects
Base: /api/v1/projects

1. GET /api/v1/projects
   - Query: q, limit, offset, include_tasks (bool)
   - Response: 200, JSON array of ProjectRead
   - Use: list and search projects

2. POST /api/v1/projects
   - Body: ProjectCreate { name, description } 
   - Response: 201 Created, Location header /api/v1/projects/{id}

3. GET /api/v1/projects/{project_id}
   - Response: 200 or 404

4. PATCH /api/v1/projects/{project_id}
   - Body: Partial fields
   - Response: 200 or 404 or 400

5. DELETE /api/v1/projects/{project_id}
   - Response: 204 No Content or 404

## Tasks (nested under project)
Base: /api/v1/projects/{project_id}/tasks

1. GET /api/v1/projects/{project_id}/tasks
   - Query: q, status, due_before, due_after, limit, offset, sort
   - Response: 200 JSON array of TaskRead

2. POST /api/v1/projects/{project_id}/tasks
   - Body: TaskCreate { title, description?, deadline?, status? }
   - Response: 201 Created, Location header /api/v1/projects/{project_id}/tasks/{id}

3. GET /api/v1/projects/{project_id}/tasks/{task_id}
   - Response: 200 or 404

4. PATCH /api/v1/projects/{project_id}/tasks/{task_id}
   - Body: TaskUpdate
   - Response: 200 or 400 or 404

5. DELETE /api/v1/projects/{project_id}/tasks/{task_id}
   - Response: 204 or 404

6. POST /api/v1/tasks/autoclose
   - Run auto-close overdue tasks (optional authenticated job or scheduled agent)
   - Response: 200 { closed: n }

## Users
Base: /api/v1/users

1. GET /api/v1/users
   - Query: q, limit, offset
   - Response: 200

2. POST /api/v1/users
   - Body: { email, name, password }
   - Response: 201, Location header /api/v1/users/{id}

3. GET /api/v1/users/{user_id}
   - Response: 200 or 404

4. PATCH /api/v1/users/{user_id}
   - Body: { name?, password? } (or PATCH semantics)
   - Response: 200 or 400 or 404

5. DELETE /api/v1/users/{user_id}
   - Response: 204 No Content

## REST Best Practices applied
- Use HTTP verbs meaningfully, resources are nouns and plural.
- Use HTTP status codes: 201 Created (with Location), 204 No Content, 400 Bad Request, 404 Not Found, 409 Conflict, 500 Internal Server Error.
- Use versioned path prefix `/api/v1/` (compatible with future changes).
- Use pagination (`limit`, `offset`) and provide total counts via `X-Total-Count` and `Link` response header for navigation.
- Provide filtering (`status`, `due_before`, `due_after`) and full-text `q` search for list endpoints.
- Use `PATCH` for partial updates and `PUT` for full updates (non-destructive), favoring `PATCH` here for partial updates.
- Prefer JSON with precise error messages. Map domain exceptions to proper HTTP codes.
- Keep services independent of controllers; call Service layer from routes so Controllers only focus on request/response.
- Use pagination and database-level filters in the service/repositories for performance.
- Provide authentication and authorization on user endpoints and any write operation.
- Use proper rate-limiting, authorization, and request validation on API.
