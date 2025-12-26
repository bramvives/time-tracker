from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    """Represents a project in the time tracking system"""
    
    id: Optional[int]
    name: str
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @classmethod
    def from_db_row(cls, row: tuple) -> "Project":
        """Create Project instance from database row"""
        return cls(
            id=row[0],
            name=row[1],
            created_at=datetime.fromisoformat(row[2]) if row[2] else None
        )