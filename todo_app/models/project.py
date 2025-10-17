from datetime import datetime
from typing import Optional

class Project:    
    _id_counter = 1
    
    def __init__(self, name: str, description: Optional[str] = None):
        self.id = Project._id_counter
        Project._id_counter += 1
        self.name = name
        self.description = description or ""
        self.created_at = datetime.now()
        self.tasks = []
    
    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}')"
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'task_count': len(self.tasks)
        }
