from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class TimeEntry:
    """Represents a time entry in the time tracking system"""
    
    id: Optional[int]
    project_id: int
    duration_minutes: int
    description: str
    entry_date: Optional[date] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.entry_date is None:
            self.entry_date = date.today()
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def duration_hours(self) -> float:
        """Get duration in hours"""
        return self.duration_minutes / 60.0
    
    @property
    def duration_formatted(self) -> str:
        """Get formatted duration as 'Xh Ym'"""
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        return f"{hours}h {minutes}m"
    
    @classmethod
    def from_db_row(cls, row: tuple) -> "TimeEntry":
        """Create TimeEntry instance from database row"""
        return cls(
            id=row[0],
            project_id=row[1],
            duration_minutes=row[2],
            description=row[3],
            entry_date=date.fromisoformat(row[4]) if row[4] else None,
            created_at=datetime.fromisoformat(row[5]) if row[5] else None
        )