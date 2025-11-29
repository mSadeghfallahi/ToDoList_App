from typing import Optional, List
from todo_app.app.api.v1 import schemas


class UserManager:
    """Stubbed user manager for API examples.

    This is a placeholder. Implement persistent storage (models + repository)
    for production use.
    """
    def create_user(self, email: str, name: Optional[str], password: str):
        raise NotImplementedError("User creation is not implemented yet")

    def get_user(self, user_id: int):
        raise NotImplementedError("Get user is not implemented yet")

    def list_users(self, limit: int = 10, offset: int = 0):
        raise NotImplementedError("List users is not implemented yet")

    def update_user(self, user_id: int, name: Optional[str] = None, password: Optional[str] = None):
        raise NotImplementedError("Update user is not implemented yet")

    def delete_user(self, user_id: int):
        raise NotImplementedError("Delete user is not implemented yet")
