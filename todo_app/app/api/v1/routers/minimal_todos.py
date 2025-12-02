from fastapi import APIRouter, HTTPException, Query, Depends, Response, status
from typing import List, Optional
from todo_app.app.api.v1 import schemas
from todo_app.services import ProjectManager, TaskManager

router = APIRouter(prefix="", tags=["minimal-todos"])


def get_project_service() -> ProjectManager:
    return ProjectManager()


def get_task_service() -> TaskManager:
    return TaskManager(project_manager=get_project_service())


@router.get("/api/v1/lists", response_model=List[schemas.ProjectRead])
def get_lists(q: Optional[str] = Query(None), limit: int = 10, offset: int = 0, service: ProjectManager = Depends(get_project_service)):
    projects = service.list_projects()
    # Pagination (in-memory for the example)
    return projects[offset: offset + limit]


@router.post("/api/v1/lists", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_list(body: schemas.ProjectCreate, response: Response, service: ProjectManager = Depends(get_project_service)):
    project = service.create_project(body.name, body.description)
    response.headers["Location"] = f"/api/v1/lists/{project.id}"
    return project


@router.get("/api/v1/lists/{list_id}", response_model=schemas.ProjectRead)
def get_list(list_id: int, service: ProjectManager = Depends(get_project_service)):
    project = service.get_project(list_id)
    if not project:
        raise HTTPException(status_code=404, detail="List not found")
    return project


@router.get("/api/v1/lists/{list_id}/tasks", response_model=List[schemas.TaskRead])
def get_tasks(list_id: int, q: Optional[str] = Query(None), limit: int = 10, offset: int = 0, service: TaskManager = Depends(get_task_service)):
    tasks = service.list_tasks(list_id)
    return tasks[offset: offset + limit]


@router.post("/api/v1/lists/{list_id}/tasks", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(list_id: int, body: schemas.TaskCreate, response: Response, service: TaskManager = Depends(get_task_service)):
    deadline = body.deadline.isoformat() if body.deadline else None
    task = service.create_task(list_id, body.title, deadline, body.description, body.status.value)
    response.headers["Location"] = f"/api/v1/lists/{list_id}/tasks/{task.id}"
    return task


@router.get("/api/v1/lists/{list_id}/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(list_id: int, task_id: int, service: TaskManager = Depends(get_task_service)):
    task = service.get_task(list_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/api/v1/lists/{list_id}/tasks/{task_id}", response_model=schemas.TaskRead)
def patch_task(list_id: int, task_id: int, body: schemas.TaskUpdate, service: TaskManager = Depends(get_task_service)):
    deadline = body.deadline.isoformat() if body.deadline else None
    task = service.edit_task(list_id, task_id, body.title, body.description, body.status.value if body.status else None, deadline)
    return task


@router.delete("/api/v1/lists/{list_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(list_id: int, task_id: int, service: TaskManager = Depends(get_task_service)):
    service.delete_task(list_id, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/api/v1/tasks/autoclose", status_code=status.HTTP_200_OK)
def autoclose(service: TaskManager = Depends(get_task_service)):
    closed = service.auto_close_overdue()
    return {"closed": closed}
