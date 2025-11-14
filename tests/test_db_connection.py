"""Tests for database connection and setup."""
import pytest
from sqlalchemy import text

from todo_app.db.session import engine, SessionLocal, init_db
from todo_app.db.base import Base


class TestDatabaseConnection:
    """Tests for database connection."""
    
    def test_engine_connection(self):
        """Test that we can connect to the database."""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    
    def test_create_tables(self):
        """Test that tables can be created."""
        try:
            init_db()
            # If no exception is raised, tables were created
            assert True
        except Exception as e:
            pytest.fail(f"Failed to create tables: {e}")
    
    def test_session_creation(self):
        """Test that we can create a database session."""
        session = SessionLocal()
        try:
            # Try to execute a simple query
            result = session.execute(text("SELECT 1"))
            assert result.scalar() == 1
        finally:
            session.close()
    
    def test_base_metadata(self):
        """Test that Base metadata contains our tables."""
        assert "projects" in Base.metadata.tables
        assert "tasks" in Base.metadata.tables

