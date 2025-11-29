from fastapi import APIRouter, HTTPException, Query, Depends, Response, status
from typing import List, Optional
from todo_app.app.api.v1 import schemas
from todo_app.services.user_manager import UserManager

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service() -> UserManager:
    return UserManager()


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(body: schemas.UserCreate, service: UserManager = Depends(get_user_service), response: Response = None):
    try:
        user = service.create_user(body.email, body.name, body.password)
        response.headers["Location"] = f"/api/v1/users/{user.id}"
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[schemas.UserRead])
def list_users(
    q: Optional[str] = Query(None, description="Search by email or name"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: UserManager = Depends(get_user_service)
):
    try:
        users = service.list_users(limit, offset)
        # For demos, we assume `list_users` returns fully populated UserRead-like objects
        return users
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="User management not implemented")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, service: UserManager = Depends(get_user_service)):
    try:
        user = service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return user
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="User management not implemented")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, body: schemas.UserUpdate, service: UserManager = Depends(get_user_service)):
    try:
        user = service.update_user(user_id, body.name, body.password)
        return user
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="User management not implemented")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserManager = Depends(get_user_service)):
    try:
        service.delete_user(user_id)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="User management not implemented")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
