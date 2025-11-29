from fastapi import APIRouter, HTTPException, Query, Depends, Response, status
from typing import List, Optional
from todo_app.app.api.v1 import schemas
from todo_app.services.project_manager import ProjectManager
from todo_app.exceptions.service_exceptions import ValidationError, DuplicateEntityError, LimitExceededError
from todo_app.exceptions.repository_exceptions import NotFoundError, RepositoryError

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_service() -> ProjectManager:
    return ProjectManager()


@router.post("", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(body: schemas.ProjectCreate, service: ProjectManager = Depends(get_project_service), response: Response = None):
    try:
        project = service.create_project(body.name, body.description)
        # Include Location header as best practice
        response.headers["Location"] = f"/api/v1/projects/{project.id}"
        return project
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DuplicateEntityError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except LimitExceededError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[schemas.ProjectRead])
def list_projects(
    q: Optional[str] = Query(None, description="Search text for name/description"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    include_tasks: bool = Query(False, description="Include a brief task count"),
    service: ProjectManager = Depends(get_project_service)
):
    projects = service.list_projects()
    # Apply simple filtering and pagination as a sample; production code should push to DB
    if q:
        projects = [p for p in projects if q.lower() in (p.name.lower() or "") or q.lower() in (p.description.lower() if p.description else "")]
    total = len(projects)
    projects = projects[offset: offset + limit]
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, service: ProjectManager = Depends(get_project_service)):
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")
    return project


@router.patch("/{project_id}", response_model=schemas.ProjectRead)
def update_project(project_id: int, body: schemas.ProjectUpdate, service: ProjectManager = Depends(get_project_service)):
    try:
        project = service.edit_project(project_id, body.name, body.description)
        return project
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, service: ProjectManager = Depends(get_project_service)):
    try:
        service.delete_project(project_id)
    except ValidationError:
        # The service uses ValidationError for not-found; map to 404
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))
