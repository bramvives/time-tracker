import sqlite3
import os
import csv
from typing import List, Optional, Tuple
from ..models import Project, TimeEntry


class Database:
    """Database class for managing SQLite operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_directory()
        self._init_tables()
    
    def _ensure_directory(self):
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    def _init_tables(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS time_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    entry_date DATE DEFAULT CURRENT_DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            """)
            
            conn.commit()
    
    # Project methods
    def create_project(self, name: str) -> bool:
        """Create a new project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO projects (name) VALUES (?)", (name,))
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_project_by_id(self, project_id: int) -> Optional[Tuple]:
        """Get project by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, created_at FROM projects WHERE id = ?", 
                (project_id,)
            )
            return cursor.fetchone()
    
    def get_project_by_name(self, name: str) -> Optional[Tuple]:
        """Get project by name"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, created_at FROM projects WHERE name = ?", 
                (name,)
            )
            return cursor.fetchone()
    
    def get_all_projects(self) -> List[Tuple]:
        """Get all projects"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, created_at FROM projects ORDER BY name"
            )
            return cursor.fetchall()
    
    def update_project(self, project_id: int, new_name: str) -> bool:
        """Update project name"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "UPDATE projects SET name = ? WHERE id = ?", 
                    (new_name, project_id)
                )
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_project(self, project_id: int) -> bool:
        """Delete project"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            return cursor.rowcount > 0
    
    # Time entry methods
    def create_time_entry(self, project_id: int, duration_minutes: int, 
                         description: str, entry_date: Optional[str] = None) -> bool:
        """Create a new time entry"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                if entry_date:
                    conn.execute(
                        "INSERT INTO time_entries (project_id, duration_minutes, description, entry_date) VALUES (?, ?, ?, ?)",
                        (project_id, duration_minutes, description, entry_date)
                    )
                else:
                    conn.execute(
                        "INSERT INTO time_entries (project_id, duration_minutes, description) VALUES (?, ?, ?)",
                        (project_id, duration_minutes, description)
                    )
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_time_entry_by_id(self, entry_id: int) -> Optional[Tuple]:
        """Get time entry by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, project_id, duration_minutes, description, entry_date, created_at FROM time_entries WHERE id = ?",
                (entry_id,)
            )
            return cursor.fetchone()
    
    def get_time_entries_by_project(self, project_id: int) -> List[Tuple]:
        """Get all time entries for a project"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, project_id, duration_minutes, description, entry_date, created_at FROM time_entries WHERE project_id = ? ORDER BY entry_date DESC",
                (project_id,)
            )
            return cursor.fetchall()
    
    def get_all_time_entries(self) -> List[Tuple]:
        """Get all time entries with project names"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT te.id, te.project_id, p.name as project_name, te.duration_minutes, 
                   te.description, te.entry_date, te.created_at 
                   FROM time_entries te 
                   JOIN projects p ON te.project_id = p.id 
                   ORDER BY te.entry_date DESC"""
            )
            return cursor.fetchall()
    
    def update_time_entry(self, entry_id: int, duration_minutes: Optional[int] = None, 
                         description: Optional[str] = None, entry_date: Optional[str] = None) -> bool:
        """Update time entry"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                updates = []
                values = []
                
                if duration_minutes is not None:
                    updates.append("duration_minutes = ?")
                    values.append(duration_minutes)
                
                if description is not None:
                    updates.append("description = ?")
                    values.append(description)
                
                if entry_date is not None:
                    updates.append("entry_date = ?")
                    values.append(entry_date)
                
                if not updates:
                    return False
                
                values.append(entry_id)
                query = f"UPDATE time_entries SET {', '.join(updates)} WHERE id = ?"
                
                cursor = conn.execute(query, values)
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_time_entry(self, entry_id: int) -> bool:
        """Delete time entry"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM time_entries WHERE id = ?", (entry_id,))
            return cursor.rowcount > 0
    
    def get_project_total_time(self, project_id: int) -> int:
        """Get total time spent on a project in minutes"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT SUM(duration_minutes) FROM time_entries WHERE project_id = ?",
                (project_id,)
            )
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
    
    def export_to_csv(self, filename: str, project_id: Optional[int] = None) -> bool:
        """Export time entries to CSV file"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                if project_id:
                    cursor = conn.execute(
                        """SELECT te.id, p.name as project_name, te.duration_minutes, 
                           te.description, te.entry_date, te.created_at 
                           FROM time_entries te 
                           JOIN projects p ON te.project_id = p.id 
                           WHERE te.project_id = ?
                           ORDER BY te.entry_date DESC""",
                        (project_id,)
                    )
                else:
                    cursor = conn.execute(
                        """SELECT te.id, p.name as project_name, te.duration_minutes, 
                           te.description, te.entry_date, te.created_at 
                           FROM time_entries te 
                           JOIN projects p ON te.project_id = p.id 
                           ORDER BY te.entry_date DESC"""
                    )
                
                data = cursor.fetchall()
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Project', 'Duration (minutes)', 'Description', 'Date', 'Created At'])
                    writer.writerows(data)
                
                return True
        except Exception:
            return False