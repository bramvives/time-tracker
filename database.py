import sqlite3
import os


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_directory()
        self._init_tables()
    
    def _ensure_directory(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    def _init_tables(self):
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
    
    def create_project(self, name: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO projects (name) VALUES (?)", (name,))
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_project_by_id(self, project_id: int) -> tuple:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, created_at FROM projects WHERE id = ?", 
                (project_id,)
            )
            return cursor.fetchone()
    
    def get_project_by_name(self, name: str) -> tuple:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, created_at FROM projects WHERE name = ?", 
                (name,)
            )
            return cursor.fetchone()
    
    def get_all_projects(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, created_at FROM projects ORDER BY name"
            )
            return cursor.fetchall()
    
    def update_project(self, project_id: int, new_name: str) -> bool:
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
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            return cursor.rowcount > 0