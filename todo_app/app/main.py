from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from todo_app.app.api.v1 import router as api_v1
from todo_app.exceptions.base import TodoAppException
from todo_app.exceptions.service_exceptions import ValidationError, ServiceError
from todo_app.exceptions.repository_exceptions import NotFoundError, RepositoryError

app = FastAPI(title="To-Do API", version="1.0.0")
app.include_router(api_v1)


@app.exception_handler(TodoAppException)
async def todo_app_exception_handler(request: Request, exc: TodoAppException):
    # Map exceptions to HTTP status codes
    if isinstance(exc, ValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, NotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, RepositoryError) or isinstance(exc, ServiceError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(status_code=status_code, content=exc.to_dict())
