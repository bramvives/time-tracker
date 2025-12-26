import click
from datetime import date


@click.group()
def time():
    """Time entry management commands"""
    pass


@time.command("add")
@click.argument("project_id", type=int, required=False)
@click.argument("duration", type=int, required=False)
@click.argument("description", required=False)
@click.option("--date", default=None, help="Date for the entry (YYYY-MM-DD). Defaults to today.")
@click.pass_context
def time_add(ctx, project_id, duration, description, date):
    """Add a new time entry to a project"""
    db = ctx.obj['db']
    
    if not project_id:
        projects = db.get_all_projects()
        if not projects:
            click.echo("No projects found. Create a project first.")
            return
        
        click.echo("Available projects:")
        for pj in projects:
            click.echo(f"  {pj[0]}: {pj[1]}")
        
        project_id = click.prompt("Project ID", type=int)
    
    project = db.get_project_by_id(project_id)
    if not project:
        click.echo(f"Project {project_id} not found.")
        return
    
    if not duration:
        duration = click.prompt("Duration in minutes", type=int)
    
    if not description:
        description = click.prompt("Description")
    
    if db.create_time_entry(project_id, duration, description, date):
        click.echo(f"Time entry added: {duration} minutes for project '{project[1]}'")
    else:
        click.echo("Failed to add time entry.")


@time.command("list")
@click.option("--project-id", type=int, help="Filter by project ID")
@click.pass_context
def time_list(ctx, project_id):
    """List time entries"""
    db = ctx.obj['db']
    
    if project_id:
        entries = db.get_time_entries_by_project(project_id)
        project = db.get_project_by_id(project_id)
        if not project:
            click.echo(f"Project {project_id} not found.")
            return
        click.echo(f"Time entries for project '{project[1]}':")
    else:
        entries = db.get_all_time_entries()
        click.echo("All time entries:")
    
    if not entries:
        click.echo("No time entries found.")
        return
    
    total_minutes = 0
    for entry in entries:
        if project_id:
            click.echo(f"  {entry[0]}: {entry[2]} min - {entry[3]} ({entry[4]})")
            total_minutes += entry[2]
        else:
            click.echo(f"  {entry[0]}: [{entry[2]}] {entry[3]} min - {entry[4]} ({entry[5]})")
            total_minutes += entry[3]
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    click.echo(f"\nTotal time: {hours}h {minutes}m ({total_minutes} minutes)")


@time.command("update")
@click.argument("entry_id", type=int, required=False)
@click.option("--duration", type=int, help="New duration in minutes")
@click.option("--description", help="New description")
@click.option("--date", help="New date (YYYY-MM-DD)")
@click.pass_context
def time_update(ctx, entry_id, duration, description, date):
    """Update a time entry"""
    db = ctx.obj['db']
    
    if not entry_id:
        entries = db.get_all_time_entries()
        if not entries:
            click.echo("No time entries found.")
            return
        
        click.echo("Available time entries:")
        for entry in entries:
            click.echo(f"  {entry[0]}: [{entry[2]}] {entry[3]} min - {entry[4]} ({entry[5]})")
        
        entry_id = click.prompt("Entry ID to update", type=int)
    
    entry = db.get_time_entry_by_id(entry_id)
    if not entry:
        click.echo(f"Time entry {entry_id} not found.")
        return
    
    click.echo(f"Current entry: {entry[2]} min - {entry[3]} ({entry[4]})")
    
    if duration is None:
        duration = click.prompt("New duration in minutes", type=int, default=entry[2])
    
    if description is None:
        description = click.prompt("New description", default=entry[3])
    
    if date is None:
        date = click.prompt("New date (YYYY-MM-DD)", default=entry[4])
    
    if db.update_time_entry(entry_id, duration, description, date):
        click.echo(f"Time entry {entry_id} updated successfully.")
    else:
        click.echo(f"Failed to update time entry {entry_id}.")


@time.command("delete")
@click.argument("entry_id", type=int, required=False)
@click.pass_context
def time_delete(ctx, entry_id):
    """Delete a time entry"""
    db = ctx.obj['db']
    
    if not entry_id:
        entries = db.get_all_time_entries()
        if not entries:
            click.echo("No time entries found.")
            return
        
        click.echo("Available time entries:")
        for entry in entries:
            click.echo(f"  {entry[0]}: [{entry[2]}] {entry[3]} min - {entry[4]} ({entry[5]})")
        
        entry_id = click.prompt("Entry ID to delete", type=int)
    
    entry = db.get_time_entry_by_id(entry_id)
    if not entry:
        click.echo(f"Time entry {entry_id} not found.")
        return
    
    if click.confirm(f"Are you sure you want to delete entry: {entry[2]} min - {entry[3]} ({entry[4]})?"):
        if db.delete_time_entry(entry_id):
            click.echo(f"Time entry {entry_id} deleted.")
        else:
            click.echo(f"Time entry {entry_id} not found.")


@time.command("summary")
@click.option("--project-id", type=int, help="Show summary for specific project")
@click.pass_context
def time_summary(ctx, project_id):
    """Show time summary by project"""
    db = ctx.obj['db']
    
    if project_id:
        project = db.get_project_by_id(project_id)
        if not project:
            click.echo(f"Project {project_id} not found.")
            return
        
        total_minutes = db.get_project_total_time(project_id)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        click.echo(f"Time summary for project '{project[1]}':")
        click.echo(f"Total time: {hours}h {minutes}m ({total_minutes} minutes)")
    else:
        projects = db.get_all_projects()
        if not projects:
            click.echo("No projects found.")
            return
        
        click.echo("Time summary by project:")
        grand_total = 0
        
        for project in projects:
            total_minutes = db.get_project_total_time(project[0])
            hours = total_minutes // 60
            minutes = total_minutes % 60
            grand_total += total_minutes
            
            click.echo(f"  {project[1]}: {hours}h {minutes}m ({total_minutes} minutes)")
        
        grand_hours = grand_total // 60
        grand_minutes = grand_total % 60
        click.echo(f"\nGrand total: {grand_hours}h {grand_minutes}m ({grand_total} minutes)")


@time.command("export")
@click.argument("filename", required=False)
@click.option("--project-id", type=int, help="Export only entries for specific project")
@click.pass_context
def time_export(ctx, filename, project_id):
    """Export time entries to CSV file"""
    db = ctx.obj['db']
    
    if not filename:
        filename = click.prompt("CSV filename")
    
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    if project_id:
        project = db.get_project_by_id(project_id)
        if not project:
            click.echo(f"Project {project_id} not found.")
            return
        
        if db.export_to_csv(filename, project_id):
            click.echo(f"Time entries for project '{project[1]}' exported to {filename}")
        else:
            click.echo("Failed to export CSV file.")
    else:
        if db.export_to_csv(filename):
            click.echo(f"All time entries exported to {filename}")
        else:
            click.echo("Failed to export CSV file.")