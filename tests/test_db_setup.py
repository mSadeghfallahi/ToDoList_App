#!/usr/bin/env python3
"""
Simple test script to verify database setup and models.
Run this script to test if everything is working correctly.
"""
import sys
from datetime import datetime, timedelta, timezone
from todo_app.db.session import engine, SessionLocal, init_db
from todo_app.models import Project, Task, TaskStatus


def test_database_connection():
    """Test if we can connect to the database."""
    print("Testing database connection...")
    try:
        with engine.connect() as conn:
            print("✓ Database connection successful!")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


def test_create_tables():
    """Test creating database tables."""
    print("\nCreating database tables...")
    try:
        init_db()
        print("✓ Tables created successfully!")
        return True
    except Exception as e:
        print(f"✗ Failed to create tables: {e}")
        return False


def test_create_project():
    """Test creating a project."""
    print("\nTesting Project creation...")
    db = SessionLocal()
    try:
        project = Project(
            name="Test Project",
            description="This is a test project"
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        print(f"✓ Project created: {project}")
        return project
    except Exception as e:
        db.rollback()
        print(f"✗ Failed to create project: {e}")
        return None
    finally:
        db.close()


def test_create_task(project_id):
    """Test creating a task."""
    print("\nTesting Task creation...")
    db = SessionLocal()
    try:
        task = Task(
            name="Test Task",
            description="This is a test task",
            status=TaskStatus.TODO,
            deadline=datetime.now(timezone.utc) + timedelta(days=7),
            project_id=project_id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        print(f"✓ Task created: {task}")
        return task
    except Exception as e:
        db.rollback()
        print(f"✗ Failed to create task: {e}")
        return None
    finally:
        db.close()


def test_relationships(project_id):
    """Test Project-Task relationship."""
    print("\nTesting Project-Task relationships...")
    db = SessionLocal()
    try:
        # Get project with tasks
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            print(f"✓ Project found: {project.name}")
            print(f"✓ Number of tasks: {len(project.tasks)}")
            for task in project.tasks:
                print(f"  - Task: {task.name} (Status: {task.status.value})")
            
            # Test reverse relationship
            if project.tasks:
                task = project.tasks[0]
                print(f"✓ Task's project: {task.project.name}")
                return True
        return False
    except Exception as e:
        print(f"✗ Relationship test failed: {e}")
        return False
    finally:
        db.close()


def test_query_operations():
    """Test querying operations."""
    print("\nTesting query operations...")
    db = SessionLocal()
    try:
        # Query all projects
        projects = db.query(Project).all()
        print(f"✓ Found {len(projects)} project(s)")
        
        # Query all tasks
        tasks = db.query(Task).all()
        print(f"✓ Found {len(tasks)} task(s)")
        
        # Query tasks by status
        todo_tasks = db.query(Task).filter(Task.status == TaskStatus.TODO).all()
        print(f"✓ Found {len(todo_tasks)} TODO task(s)")
        
        return True
    except Exception as e:
        print(f"✗ Query operations failed: {e}")
        return False
    finally:
        db.close()


def cleanup_test_data():
    """Clean up test data."""
    print("\nCleaning up test data...")
    db = SessionLocal()
    try:
        # Delete test projects (tasks will be deleted due to CASCADE)
        test_projects = db.query(Project).filter(Project.name.like("Test%")).all()
        for project in test_projects:
            db.delete(project)
        db.commit()
        print(f"✓ Cleaned up {len(test_projects)} test project(s)")
    except Exception as e:
        db.rollback()
        print(f"✗ Cleanup failed: {e}")
    finally:
        db.close()


def main():
    """Run all tests."""
    print("=" * 50)
    print("Database Setup and Models Test")
    print("=" * 50)
    
    # Test database connection
    if not test_database_connection():
        print("\n❌ Database connection failed. Make sure:")
        print("  1. Docker container is running: docker-compose up -d")
        print("  2. .env file exists with correct database credentials")
        sys.exit(1)
    
    # Create tables
    if not test_create_tables():
        print("\n❌ Failed to create tables.")
        sys.exit(1)
    
    # Test creating project
    project = test_create_project()
    if not project:
        print("\n❌ Failed to create project.")
        sys.exit(1)
    
    # Test creating task
    task = test_create_task(project.id)
    if not task:
        print("\n❌ Failed to create task.")
        sys.exit(1)
    
    # Test relationships
    if not test_relationships(project.id):
        print("\n❌ Relationship test failed.")
        sys.exit(1)
    
    # Test query operations
    if not test_query_operations():
        print("\n❌ Query operations failed.")
        sys.exit(1)
    
    # Cleanup (optional - comment out if you want to keep test data)
    # cleanup_test_data()
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    main()

