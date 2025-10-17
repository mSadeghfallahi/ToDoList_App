from typing import List, Optional
from todo_app.models.project import Project
from todo_app.utils.validators import Validator, ValidationError
from todo_app.config import Config

class ProjectManager:
    """Service layer for managing projects"""
    
    def __init__(self):
        self.projects: List[Project] = []
    
    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        """Create a new project"""
        # Validate max projects
        if len(self.projects) >= Config.MAX_NUMBER_OF_PROJECTS:
            raise ValidationError(f"Maximum number of projects ({Config.MAX_NUMBER_OF_PROJECTS}) reached")
        
        # Validate name
        is_valid, error = Validator.validate_name(name)
        if not is_valid:
            raise ValidationError(error)
        
        # Check uniqueness
        if self._is_name_exists(name):
            raise ValidationError(f"Project with name '{name}' already exists")
        
        # Validate description
        is_valid, error = Validator.validate_description(description)
        if not is_valid:
            raise ValidationError(error)
        
        project = Project(name, description)
        self.projects.append(project)
        return project
    
    def edit_project(self, project_id: int, name: Optional[str] = None, 
                    description: Optional[str] = None) -> Project:
        """Edit an existing project"""
        project = self._get_project_by_id(project_id)
        if not project:
            raise ValidationError(f"Project with ID {project_id} not found")
        
        # Validate and update name if provided
        if name is not None:
            is_valid, error = Validator.validate_name(name)
            if not is_valid:
                raise ValidationError(error)
            
            # Check uniqueness (excluding current project)
            if self._is_name_exists(name, exclude_id=project_id):
                raise ValidationError(f"Project with name '{name}' already exists")
            
            project.name = name
        
        # Validate and update description if provided
        if description is not None:
            is_valid, error = Validator.validate_description(description)
            if not is_valid:
                raise ValidationError(error)
            
            project.description = description
        
        return project
    
    def delete_project(self, project_id: int) -> bool:
        """Delete a project (cascade delete tasks)"""
        project = self._get_project_by_id(project_id)
        if not project:
            raise ValidationError(f"Project with ID {project_id} not found")
        
        self.projects.remove(project)
        return True
    
    def list_projects(self) -> List[Project]:
        """List all projects sorted by creation date"""
        return sorted(self.projects, key=lambda p: p.created_at)
    
    def _get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        for project in self.projects:
            if project.id == project_id:
                return project
        return None
    
    def _is_name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if project name already exists"""
        for project in self.projects:
            if exclude_id and project.id == exclude_id:
                continue
            if project.name.lower() == name.lower():
                return True
        return False