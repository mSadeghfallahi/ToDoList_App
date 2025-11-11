"""Database session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from todo_app.config import Config
from .base import Base


# Create SQLAlchemy engine
# The database URL is constructed from environment variables via Config
engine = create_engine(
    Config.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Maximum number of connections beyond pool_size
)

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

