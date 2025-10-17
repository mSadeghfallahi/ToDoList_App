from typing import List, Optional
from datetime import datetime
from todo_app.models.task import Task
from todo_app.models.project import Project
from todo_app.utils.validators import Validator, ValidationError

class TaskManager:
    def __init__(self, project_manager):
        self.project_manager = project_manager
    
    def create_task(self, project_id: int, title: str, deadline: str,
                   description: Optional[str] = None, status: str = 'to-do') -> Task:
        """Create a new task"""
        # Get project
        project = self._get_project(project_id)
        
        # Validate title
        is_valid, error = Validator.validate_name(title, max_words=30)
        if not is_valid:
            raise ValidationError(error)
        
        # Validate description
        is_valid, error = Validator.validate_description(description, max_words=150)
        if not is_valid:
            raise ValidationError(error)
        
        # Validate status
        is_valid, error = Validator.validate_status(status)
        if not is_valid:
            raise ValidationError(error)
        
        # Validate deadline
        is_valid, error, deadline_obj = Validator.validate_date(deadline)
        if not is_valid:
            raise ValidationError(error)
        
        task = Task(title, project_id, deadline_obj, description, status)
        project.tasks.append(task)
        return task
    
    def edit_task(self, project_id: int, task_id: int, 
                 title: Optional[str] = None, description: Optional[str] = None,
                 status: Optional[str] = None, deadline: Optional[str] = None) -> Task:
        """Edit an existing task"""
        project = self._get_project(project_id)
        task = self._get_task(project, task_id)
        
        # Validate and update title if provided
        if title is not None:
            is_valid, error = Validator.validate_name(title, max_words=30)
            if not is_valid:
                raise ValidationError(error)
            task.title = title
        
        # Validate and update description if provided
        if description is not None:
            is_valid, error = Validator.validate_description(description, max_words=150)
            if not is_valid:
                raise ValidationError(error)
            task.description = description
        
        # Validate and update status if provided
        if status is not None:
            is_valid, error = Validator.validate_status(status)
            if not is_valid:
                raise ValidationError(error)
            task.status = status.lower()
        
        # Validate and update deadline if provided
        if deadline is not None:
            is_valid, error, deadline_obj = Validator.validate_date(deadline)
            if not is_valid:
                raise ValidationError(error)
            task.deadline = deadline_obj
        
        return task
    
    def delete_task(self, project_id: int, task_id: int) -> bool:
        """Delete a task"""
        project = self._get_project(project_id)
        task = self._get_task(project, task_id)
        
        project.tasks.remove(task)
        return True
    
    def list_tasks(self, project_id: int) -> List[Task]:
        """List all tasks in a project"""
        project = self._get_project(project_id)
        return project.tasks
    
    def _get_project(self, project_id: int) -> Project:
        """Get project by ID"""
        for project in self.project_manager.projects:
            if project.id == project_id:
                return project
        raise ValidationError(f"Project with ID {project_id} not found")
    
    def _get_task(self, project: Project, task_id: int) -> Task:
        """Get task by ID"""
        for task in project.tasks:
            if task.id == task_id:
                return task
        raise ValidationError(f"Task with ID {task_id} not found")