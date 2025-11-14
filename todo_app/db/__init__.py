"""Database package for the ToDo application.

This package intentionally does not import the session/engine at package
import time to avoid eagerly creating a database engine when importing
submodules (e.g. model classes). Import the lower-level helpers directly
from `todo_app.db.session` when you need to create sessions or access the
engine.
"""
from .base import Base

__all__ = ["Base"]

