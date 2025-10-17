from datetime import datetime
from typing import Optional, Tuple

class ValidationError(Exception):
    pass

class Validator:    
    @staticmethod
    def validate_name(name: str, max_words: int = 30) -> Tuple[bool, Optional[str]]:
        """Validate project/task name"""
        if not name or not name.strip():
            return False, "Name cannot be empty"
        
        word_count = len(name.split())
        if word_count > max_words:
            return False, f"Name must be less than {max_words} words (current: {word_count})"
        
        return True, None
    
    @staticmethod
    def validate_description(description: Optional[str], max_words: int = 150) -> Tuple[bool, Optional[str]]:
        """Validate description"""
        if description is None or not description.strip():
            return True, None  # Description is optional
        
        word_count = len(description.split())
        if word_count > max_words:
            return False, f"Description must be less than {max_words} words (current: {word_count})"
        
        return True, None
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, Optional[str], Optional[datetime]]:
        """Validate date format (YYYY-MM-DD)"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return True, None, date_obj
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-31)", None
    
    @staticmethod
    def validate_status(status: str) -> Tuple[bool, Optional[str]]:
        """Validate task status"""
        valid_statuses = ['to-do', 'doing', 'done']
        status_lower = status.lower()
        
        if status_lower not in valid_statuses:
            return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        
        return True, None