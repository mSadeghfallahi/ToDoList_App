from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from todo_app.models.project import Project
from todo_app.utils.validators import Validator, ValidationError
from todo_app.config import Config
from todo_app.db.session import SessionLocal, init_db


class ProjectManager:
    """Service layer for managing projects"""
    
    def __init__(self):
        # Initialize database on first use
        init_db()
    
    def _get_db(self) -> Session:
        """Get database session"""
        return SessionLocal()
    
    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        """Create a new project"""
        db = self._get_db()
        
        try:
            # Validate max projects
            stmt = select(Project)
            projects = db.scalars(stmt).all()
            if len(projects) >= Config.MAX_NUMBER_OF_PROJECTS:
                raise ValidationError(f"Maximum number of projects ({Config.MAX_NUMBER_OF_PROJECTS}) reached")
            
            # Validate name
            is_valid, error = Validator.validate_name(name)
            if not is_valid:
                raise ValidationError(error)
            
            # Check uniqueness
            if self._is_name_exists(db, name):
                raise ValidationError(f"Project with name '{name}' already exists")
            
            # Validate description
            is_valid, error = Validator.validate_description(description)
            if not is_valid:
                raise ValidationError(error)
            
            # Create project using keyword arguments
            project = Project(name=name, description=description)
            db.add(project)
            db.commit()
            db.refresh(project)
            # Access attributes to load them before session closes
            _ = project.id, project.name, project.description, project.created_at, project.updated_at
            # Expunge to detach from session
            db.expunge(project)
            return project
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    def edit_project(self, project_id: int, name: Optional[str] = None, 
                    description: Optional[str] = None) -> Project:
        """Edit an existing project"""
        db = self._get_db()
        
        try:
            project = db.get(Project, project_id)
            if not project:
                raise ValidationError(f"Project with ID {project_id} not found")
            
            # Validate and update name if provided
            if name is not None:
                is_valid, error = Validator.validate_name(name)
                if not is_valid:
                    raise ValidationError(error)
                
                # Check uniqueness (excluding current project)
                if self._is_name_exists(db, name, exclude_id=project_id):
                    raise ValidationError(f"Project with name '{name}' already exists")
                
                project.name = name
            
            # Validate and update description if provided
            if description is not None:
                is_valid, error = Validator.validate_description(description)
                if not is_valid:
                    raise ValidationError(error)
                
                project.description = description
            
            db.commit()
            db.refresh(project)
            # Access attributes to load them before session closes
            _ = project.id, project.name, project.description, project.created_at, project.updated_at
            # Expunge to detach from session
            db.expunge(project)
            return project
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    def delete_project(self, project_id: int) -> bool:
        """Delete a project (cascade delete tasks)"""
        db = self._get_db()
        
        try:
            project = db.get(Project, project_id)
            if not project:
                raise ValidationError(f"Project with ID {project_id} not found")
            
            db.delete(project)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    def list_projects(self) -> List[Project]:
        """List all projects sorted by creation date"""
        db = self._get_db()
        
        try:
            # Eagerly load tasks relationship
            stmt = select(Project).options(joinedload(Project.tasks)).order_by(Project.created_at)
            projects = db.scalars(stmt).unique().all()
            projects_list = list(projects)
            # Access attributes and expunge to detach from session
            for p in projects_list:
                _ = p.id, p.name, p.description, p.created_at, len(p.tasks)
                db.expunge(p)
            return projects_list
        finally:
            db.close()
    
    def _get_project_by_id(self, db: Session, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return db.get(Project, project_id)
    
    def _is_name_exists(self, db: Session, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if project name already exists"""
        stmt = select(Project).where(Project.name.ilike(name))
        if exclude_id:
            stmt = stmt.where(Project.id != exclude_id)
        project = db.scalar(stmt)
        return project is not None
