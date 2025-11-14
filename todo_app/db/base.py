"""SQLAlchemy declarative base for ORM models."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    
    All model classes should inherit from this Base class to enable
    SQLAlchemy ORM functionality.
    """
    pass

