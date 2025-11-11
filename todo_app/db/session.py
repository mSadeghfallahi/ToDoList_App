"""Database session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from todo_app.config import Config
from .base import Base


# Build engine kwargs conditionally so that tests can use SQLite in-memory
# without passing invalid pool arguments for that dialect.
engine_kwargs = {
    'echo': False,
    'pool_pre_ping': True,
}

# If the configured URL is not SQLite, it's safe to set pool sizing options.
if not Config.DATABASE_URL.startswith('sqlite:'):
    engine_kwargs.update({'pool_size': 5, 'max_overflow': 10})

# Create SQLAlchemy engine using the computed kwargs
engine = create_engine(Config.DATABASE_URL, **engine_kwargs)

# Create SessionLocal factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator:
    """
    Dependency function to get a database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage:
        db = next(get_db())
        # Use db session
        db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    
    This should be called once to create the database schema.
    """
    Base.metadata.create_all(bind=engine)

