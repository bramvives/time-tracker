# Time Tracker CLI

A command-line application for tracking time spent on projects. Built with Python and SQLite, this tool allows you to manage projects and log time entries with detailed descriptions.

## Features

- **Project Management**: Create, list, update, and delete projects
- **Time Tracking**: Add, list, update, and delete time entries
- **Reporting**: View time summaries by project
- **Data Export**: Export time entries to CSV format
- **Interactive CLI**: User-friendly command-line interface with prompts
- **SQLite Database**: Lightweight, file-based database storage

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository** (or download the project files):
   ```bash
   git clone https://github.com/bramvives/time-tracker
   cd time-tracker
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**:
   ```bash
   # Copy the example config file
   cp data/config.example.json data/config.json
   ```
   
   Edit `data/config.json` if needed to change the database location:
   ```json
   {
     "db_path": "./data/db.sqlite"
   }
   ```

## Usage

Run the application using:
```bash
python app.py [COMMAND] [OPTIONS]
```

### Available Commands

#### Project Management

**List all projects:**
```bash
python app.py project list
```

**Add a new project:**
```bash
python app.py project add "My Project"
# or interactively:
python app.py project add
```

**Update a project name:**
```bash
python app.py project update 1 "New Project Name"
# or interactively:
python app.py project update
```

**Delete a project:**
```bash
python app.py project delete 1
# or interactively:
python app.py project delete
```

#### Time Entry Management

**Add a time entry:**
```bash
python app.py time add 1 120 "Working on feature X"
# or interactively:
python app.py time add
```

**List all time entries:**
```bash
python app.py time list
```

**List entries for a specific project:**
```bash
python app.py time list --project-id 1
```

**Update a time entry:**
```bash
python app.py time update 1 --duration 150 --description "Updated description"
# or interactively:
python app.py time update
```

**Delete a time entry:**
```bash
python app.py time delete 1
# or interactively:
python app.py time delete
```

#### Reporting

**View time summary for all projects:**
```bash
python app.py time summary
```

**View time summary for a specific project:**
```bash
python app.py time summary --project-id 1
```

#### Data Export

**Export all time entries to CSV:**
```bash
python app.py time export my_report.csv
```

**Export specific project to CSV:**
```bash
python app.py time export project_report.csv --project-id 1
```

## Database Structure

The application uses SQLite with two main tables:

### Projects Table
- `id`: Primary key (auto-increment)
- `name`: Project name (unique)
- `created_at`: Timestamp when project was created

### Time Entries Table
- `id`: Primary key (auto-increment)
- `project_id`: Foreign key to projects table
- `duration_minutes`: Time duration in minutes
- `description`: Description of the work done
- `entry_date`: Date of the time entry (defaults to current date)
- `created_at`: Timestamp when entry was created

## Configuration

The application uses a JSON configuration file located at `data/config.json`:

```json
{
  "db_path": "./data/db.sqlite"
}
```

- **db_path**: Path to the SQLite database file (relative or absolute)

## Examples

### Basic Workflow

1. **Create a project:**
   ```bash
   python app.py project add "Website Development"
   ```

2. **Add time entries:**
   ```bash
   python app.py time add 1 120 "Implemented user login"
   python app.py time add 1 90 "Fixed responsive design issues"
   ```

3. **View project summary:**
   ```bash
   python app.py time summary --project-id 1
   ```

4. **Export data:**
   ```bash
   python app.py time export website_dev_report.csv --project-id 1
   ```

### Sample Output

```bash
$ python app.py project list
Projects:
  1: Website Development (created: 2024-01-15 10:30:00)
  2: Mobile App (created: 2024-01-16 09:15:00)

$ python app.py time summary
Time summary by project:
  Website Development: 3h 30m (210 minutes)
  Mobile App: 2h 15m (135 minutes)

Grand total: 5h 45m (345 minutes)
```