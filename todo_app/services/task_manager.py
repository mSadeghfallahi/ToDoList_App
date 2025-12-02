from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from todo_app.models.task import Task, TaskStatus
from todo_app.models.project import Project
from todo_app.utils.validators import Validator, ValidationError
from todo_app.db.session import SessionLocal


class TaskManager:
    """Service layer for managing tasks"""
    
    def __init__(self, project_manager):
        self.project_manager = project_manager
    
    def _get_db(self) -> Session:
        """Get database session"""
        return SessionLocal()
    
    def _map_status_to_enum(self, status: str) -> TaskStatus:
        """Map status string to TaskStatus enum"""
        status_lower = status.lower()
        status_map = {
            'to-do': TaskStatus.TODO,
            'doing': TaskStatus.IN_PROGRESS,  # Map "doing" to "in-progress"
            'in-progress': TaskStatus.IN_PROGRESS,
            'done': TaskStatus.DONE,
            'cancelled': TaskStatus.CANCELLED
        }
        return status_map.get(status_lower, TaskStatus.TODO)
    
    def create_task(self, project_id: int, title: str, due_date: Optional[str] = None,
                   description: Optional[str] = None, status: Optional[str] = 'to-do', done: Optional[bool] = False) -> Task:
        """Create a new task"""
        db = self._get_db()
        
        try:
            # Get project
            project = db.get(Project, project_id)
            if not project:
                raise ValidationError(f"Project with ID {project_id} not found")
            
            # Validate title (Task model uses 'name' field)
            is_valid, error = Validator.validate_name(title, max_words=30)
            if not is_valid:
                raise ValidationError(error)
            
            # Validate description
            is_valid, error = Validator.validate_description(description, max_words=150)
            if not is_valid:
                raise ValidationError(error)
            
            # Validate status if provided
            if status is not None:
                is_valid, error = Validator.validate_status(status)
                if not is_valid:
                    raise ValidationError(error)

            # Validate due_date
            is_valid, error, deadline_obj = Validator.validate_date(due_date) if due_date else (True, None, None)
            if not is_valid:
                raise ValidationError(error)
            
            # Map 'done' boolean or status string to enum
            if done:
                status_enum = TaskStatus.DONE
            else:
                status_enum = self._map_status_to_enum(status) if status is not None else TaskStatus.TODO
            
            # Create task using keyword arguments
            task = Task(
                name=title,  # Task model uses 'name' field
                project_id=project_id,
                deadline=deadline_obj,
                description=description,
                status=status_enum
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            # Access attributes to load them before session closes
            _ = task.id, task.name, task.description, task.status, task.deadline, task.project_id, task.created_at, task.updated_at
            # Expunge to detach from session
            db.expunge(task)
            return task
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    def edit_task(self, project_id: int, task_id: int, 
                 title: Optional[str] = None, description: Optional[str] = None,
                 status: Optional[str] = None, due_date: Optional[str] = None, done: Optional[bool] = None) -> Task:
        """Edit an existing task"""
        db = self._get_db()
        
        try:
            # Verify project exists
            project = db.get(Project, project_id)
            if not project:
                raise ValidationError(f"Project with ID {project_id} not found")
            
            # Get task
            task = db.get(Task, task_id)
            if not task:
                raise ValidationError(f"Task with ID {task_id} not found")
            
            # Verify task belongs to project
            if task.project_id != project_id:
                raise ValidationError(f"Task {task_id} does not belong to project {project_id}")
            
            # Validate and update title if provided
            if title is not None:
                is_valid, error = Validator.validate_name(title, max_words=30)
                if not is_valid:
                    raise ValidationError(error)
                task.name = title  # Task model uses 'name' field
            
            # Validate and update description if provided
            if description is not None:
                is_valid, error = Validator.validate_description(description, max_words=150)
                if not is_valid:
                    raise ValidationError(error)
                task.description = description
            
            # Validate and update status/done if provided
            if done is not None:
                if done:
                    task.status = TaskStatus.DONE
                else:
                    # If explicitly set to not done, default to TODO unless status provided
                    task.status = self._map_status_to_enum(status) if status is not None else TaskStatus.TODO
            elif status is not None:
                is_valid, error = Validator.validate_status(status)
                if not is_valid:
                    raise ValidationError(error)
                task.status = self._map_status_to_enum(status)
            
            # Validate and update due_date if provided
            if due_date is not None:
                is_valid, error, deadline_obj = Validator.validate_date(due_date)
                if not is_valid:
                    raise ValidationError(error)
                task.deadline = deadline_obj
            
            db.commit()
            db.refresh(task)
            # Access attributes to load them before session closes
            _ = task.id, task.name, task.description, task.status, task.deadline, task.project_id, task.created_at, task.updated_at
            # Expunge to detach from session
            db.expunge(task)
            return task
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    def delete_task(self, project_id: int, task_id: int) -> bool:
        """Delete a task"""
        db = self._get_db()
        
        try:
            # Verify project exists
            project = db.get(Project, project_id)
            if not project:
                raise ValidationError(f"Project with ID {project_id} not found")
            
            # Get task
            task = db.get(Task, task_id)
            if not task:
                raise ValidationError(f"Task with ID {task_id} not found")
            
            # Verify task belongs to project
            if task.project_id != project_id:
                raise ValidationError(f"Task {task_id} does not belong to project {project_id}")
            
            db.delete(task)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    def list_tasks(self, project_id: int) -> List[Task]:
        """List all tasks in a project"""
        db = self._get_db()
        try:
            # Verify project exists
            project = db.get(Project, project_id)
            if not project:
                raise ValidationError(f"Project with ID {project_id} not found")
            
            stmt = select(Task).where(Task.project_id == project_id).order_by(Task.created_at)
            tasks = db.scalars(stmt).all()
            tasks_list = list(tasks)
            # Access attributes and expunge to detach from session
            for t in tasks_list:
                _ = t.id, t.name, t.description, t.status, t.deadline, t.project_id, t.created_at, t.updated_at
                db.expunge(t)
            return tasks_list
        finally:
            db.close()
    def get_task(self, project_id: int, task_id: int) -> Optional[Task]:
        """Return a single task belonging to a specified project (detached)."""
        db = self._get_db()
        try:
            task = db.get(Task, task_id)
            if not task or task.project_id != project_id:
                return None
            _ = task.id, task.name, task.description, task.status, task.deadline, task.created_at
            db.expunge(task)
            return task
        finally:
            db.close()
    def auto_close_overdue(self) -> int:
        """Auto-close overdue tasks.

        Returns the number of tasks closed.
        """
        db = self._get_db()
        try:
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)
            stmt = select(Task).where(Task.deadline < now, Task.status != TaskStatus.DONE)
            overdue_tasks = db.scalars(stmt).all()
            if not overdue_tasks:
                return 0
            closed_count = 0
            for task in overdue_tasks:
                task.status = TaskStatus.DONE
                task.updated_at = now
                closed_count += 1
            db.commit()
            return closed_count
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()