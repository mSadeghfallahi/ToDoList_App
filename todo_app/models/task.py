from datetime import datetime
from typing import Optional

class Task:
    _id_counter = 1
    
    def __init__(self, title: str, project_id: int, deadline: datetime, 
                 description: Optional[str] = None, status: str = 'to-do'):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.project_id = project_id
        self.description = description or ""
        self.status = status.lower()
        self.deadline = deadline
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'deadline': self.deadline.strftime('%Y-%m-%d'),
            'created_at': self.created_at.isoformat()
        }