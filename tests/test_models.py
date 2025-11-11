"""Tests for database models."""
import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError

from todo_app.db.session import SessionLocal, init_db
from todo_app.models import Project, Task, TaskStatus


@pytest.fixture(scope="function")
def db_session():
    """Create a database session for testing."""
    # Initialize database
    init_db()
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def sample_project(db_session):
    """Create a sample project for testing."""
    project = Project(
        name="Test Project",
        description="A test project"
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


class TestProject:
    """Tests for Project model."""
    
    def test_create_project(self, db_session):
        """Test creating a project."""
        project = Project(
            name="New Project",
            description="Project description"
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        
        assert project.id is not None
        assert project.name == "New Project"
        assert project.description == "Project description"
        assert project.created_at is not None
    
    def test_project_requires_name(self, db_session):
        """Test that project name is required."""
        project = Project(description="No name")
        db_session.add(project)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
    
    def test_project_to_dict(self, sample_project):
        """Test project to_dict method."""
        project_dict = sample_project.to_dict()
        
        assert 'id' in project_dict
        assert 'name' in project_dict
        assert 'description' in project_dict
        assert 'created_at' in project_dict
        assert 'task_count' in project_dict
        assert project_dict['name'] == "Test Project"


class TestTask:
    """Tests for Task model."""
    
    def test_create_task(self, db_session, sample_project):
        """Test creating a task."""
        task = Task(
            name="New Task",
            description="Task description",
            status=TaskStatus.TODO,
            deadline=datetime.now(timezone.utc) + timedelta(days=7),
            project_id=sample_project.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.id is not None
        assert task.name == "New Task"
        assert task.status == TaskStatus.TODO
        assert task.project_id == sample_project.id
        assert task.deadline is not None
    
    def test_task_requires_name(self, db_session, sample_project):
        """Test that task name is required."""
        task = Task(
            description="No name",
            project_id=sample_project.id
        )
        db_session.add(task)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
    
    def test_task_requires_project_id(self, db_session):
        """Test that task requires a project_id."""
        task = Task(
            name="Task without project",
            status=TaskStatus.TODO
        )
        db_session.add(task)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
    
    def test_task_status_enum(self, db_session, sample_project):
        """Test task status enum values."""
        task = Task(
            name="Test Task",
            status=TaskStatus.IN_PROGRESS,
            project_id=sample_project.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.status.value == "in-progress"
    
    def test_task_to_dict(self, db_session, sample_project):
        """Test task to_dict method."""
        task = Task(
            name="Dict Test Task",
            status=TaskStatus.DONE,
            project_id=sample_project.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        task_dict = task.to_dict()
        
        assert 'id' in task_dict
        assert 'name' in task_dict
        assert 'status' in task_dict
        assert 'project_id' in task_dict
        assert task_dict['status'] == "done"


class TestRelationships:
    """Tests for Project-Task relationships."""
    
    def test_project_has_tasks(self, db_session, sample_project):
        """Test that a project can have multiple tasks."""
        task1 = Task(
            name="Task 1",
            project_id=sample_project.id,
            status=TaskStatus.TODO
        )
        task2 = Task(
            name="Task 2",
            project_id=sample_project.id,
            status=TaskStatus.IN_PROGRESS
        )
        db_session.add_all([task1, task2])
        db_session.commit()
        
        # Refresh to load relationships
        db_session.refresh(sample_project)
        
        assert len(sample_project.tasks) == 2
        assert task1 in sample_project.tasks
        assert task2 in sample_project.tasks
    
    def test_task_belongs_to_project(self, db_session, sample_project):
        """Test that a task belongs to a project."""
        task = Task(
            name="Belongs To Test",
            project_id=sample_project.id,
            status=TaskStatus.TODO
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.project is not None
        assert task.project.id == sample_project.id
        assert task.project.name == sample_project.name
    
    def test_cascade_delete(self, db_session, sample_project):
        """Test that deleting a project deletes its tasks."""
        task = Task(
            name="Cascade Test Task",
            project_id=sample_project.id,
            status=TaskStatus.TODO
        )
        db_session.add(task)
        db_session.commit()
        
        task_id = task.id
        
        # Delete project
        db_session.delete(sample_project)
        db_session.commit()
        
        # Verify task is also deleted
        deleted_task = db_session.query(Task).filter(Task.id == task_id).first()
        assert deleted_task is None

