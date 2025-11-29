from fastapi import APIRouter
from todo_app.app.api.v1.routers import projects_router as projects, tasks_router as tasks, users_router as users

router = APIRouter(prefix="/api/v1")
router.include_router(projects)
router.include_router(tasks)
router.include_router(users)

__all__ = ["router"]
