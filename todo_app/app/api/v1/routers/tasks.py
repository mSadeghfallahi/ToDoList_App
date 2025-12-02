from fastapi import APIRouter, HTTPException, Query, Depends, Response, status
from typing import List, Optional
from datetime import datetime
from todo_app.app.api.v1 import schemas
from todo_app.services.task_manager import TaskManager
from todo_app.services.project_manager import ProjectManager
from todo_app.exceptions.service_exceptions import ValidationError
from todo_app.exceptions.repository_exceptions import NotFoundError, RepositoryError

router = APIRouter(prefix="", tags=["tasks"])


def get_task_service() -> TaskManager:
    return TaskManager(project_manager=ProjectManager())


@router.post("/projects/{project_id}/tasks", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, body: schemas.TaskCreate, service: TaskManager = Depends(get_task_service), response: Response = None):
    try:
        # TaskManager expects due_date string; convert if provided
        due_date = body.due_date.strftime('%Y-%m-%d') if body.due_date else None
        task = service.create_task(project_id, body.title, due_date, body.description, done=body.done)
        response.headers["Location"] = f"/api/v1/projects/{project_id}/tasks/{task.id}"
        return task
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/tasks", response_model=List[schemas.TaskRead])
def list_tasks(
    project_id: int,
    q: Optional[str] = Query(None, description="Search in title/description"),
    status: Optional[schemas.TaskStatus] = Query(None, description="Filter by task status"),
    due_before: Optional[datetime] = Query(None),
    due_after: Optional[datetime] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort: Optional[str] = Query("created_at"),
    service: TaskManager = Depends(get_task_service)
):
    try:
        tasks = service.list_tasks(project_id)
        # Filters (in-memory). Move to service/db for scale.
        if q:
            tasks = [t for t in tasks if q.lower() in (t.title.lower() or "") or q.lower() in (t.description.lower() if t.description else "")]
        if status:
            tasks = [t for t in tasks if (t.done and status.value == "done") or (not t.done and status.value != "done")]
        if due_before:
            tasks = [t for t in tasks if t.due_date and t.due_date <= due_before]
        if due_after:
            tasks = [t for t in tasks if t.due_date and t.due_date >= due_after]
        # Simple sorting
        if sort == "created_at":
            tasks.sort(key=lambda t: t.created_at)
        elif sort == "deadline":
            tasks.sort(key=lambda t: (t.deadline or datetime.max))
        total = len(tasks)
        return tasks[offset: offset + limit]
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(project_id: int, task_id: int, service: TaskManager = Depends(get_task_service)):
    task = service.get_task(project_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found in project {project_id}")
    return task


@router.patch("/projects/{project_id}/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(project_id: int, task_id: int, body: schemas.TaskUpdate, service: TaskManager = Depends(get_task_service)):
    try:
        due_date = body.due_date.strftime('%Y-%m-%d') if body.due_date else None
        task = service.edit_task(project_id, task_id, body.title, body.description, status=None, due_date=due_date, done=body.done)
        return task
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/projects/{project_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(project_id: int, task_id: int, service: TaskManager = Depends(get_task_service)):
    try:
        service.delete_task(project_id, task_id)
    except ValidationError:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found in project {project_id}")
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/autoclose", status_code=200)
def auto_close(service: TaskManager = Depends(get_task_service)):
    # Endpoint to trigger auto-close across all projects. In practice, use proper authentication or a scheduled job.
    closed = service.auto_close_overdue()
    return {"closed": closed}
