"""Pytest fixtures for the test suite.

This file provides fixtures that are shared across multiple test files.
"""
from __future__ import annotations

import os
import pytest

# When running tests in environments without the PostgreSQL driver available
# allow tests to use an in-memory SQLite database by setting DATABASE_URL
# before importing the application's DB session. This keeps tests hermetic
# and avoids requiring external DB drivers for unit tests.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from todo_app.db.session import SessionLocal, init_db
from todo_app.models import Project


@pytest.fixture(scope="session")
def project_id():
    """Create a temporary project for tests that require a project id.

    The fixture creates a Project in the test database and yields its id.
    After the test session completes, it attempts to delete the project.
    """
    # Ensure tables exist
    init_db()

    db = SessionLocal()
    try:
        project = Project(name="Fixture Project", description="Created by fixture")
        db.add(project)
        db.commit()
        db.refresh(project)
        pid = project.id
        yield pid
    finally:
        try:
            # Attempt to remove the fixture project if it still exists
            proj = db.get(Project, pid)
            if proj:
                db.delete(proj)
                db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()
