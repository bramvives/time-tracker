import click


@click.group()
def project():
    """Project management commands"""
    pass


@project.command("add")
@click.argument("name", required=False)
@click.pass_context
def project_add(ctx, name):
    """Add a new project"""
    if not name:
        name = click.prompt("Project name")
    
    db = ctx.obj['db']
    if db.create_project(name):
        click.echo(f"Project '{name}' created successfully.")
    else:
        click.echo(f"Project '{name}' already exists.")


@project.command("list")
@click.pass_context
def project_list(ctx):
    """List all projects"""
    db = ctx.obj['db']
    projects = db.get_all_projects()
    if not projects:
        click.echo("No projects found.")
        return
    
    click.echo("Projects:")
    for pj in projects:
        click.echo(f"  {pj[0]}: {pj[1]} (created: {pj[2]})")


@project.command("update")
@click.argument("project_id", type=int, required=False)
@click.argument("new_name", required=False)
@click.pass_context
def project_update(ctx, project_id, new_name):
    """Update a project name"""
    db = ctx.obj['db']
    
    if not project_id:
        # Show available projects
        projects = db.get_all_projects()
        if not projects:
            click.echo("No projects found.")
            return
        
        click.echo("Available projects:")
        for pj in projects:
            click.echo(f"  {pj[0]}: {pj[1]}")
        
        project_id = click.prompt("Project ID to update", type=int)
    
    if not new_name:
        # Show current project name
        current_project = db.get_project_by_id(project_id)
        if not current_project:
            click.echo(f"Project {project_id} not found.")
            return
        
        click.echo(f"Current name: {current_project[1]}")
        new_name = click.prompt("New project name")
    
    if db.update_project(project_id, new_name):
        click.echo(f"Project {project_id} renamed to '{new_name}'.")
    else:
        click.echo(f"Project {project_id} not found or '{new_name}' already exists.")


@project.command("delete")
@click.argument("project_id", type=int, required=False)
@click.pass_context
def project_delete(ctx, project_id):
    """Delete a project"""
    db = ctx.obj['db']
    
    if not project_id:
        # Show available projects
        projects = db.get_all_projects()
        if not projects:
            click.echo("No projects found.")
            return
        
        click.echo("Available projects:")
        for pj in projects:
            click.echo(f"  {pj[0]}: {pj[1]}")
        
        project_id = click.prompt("Project ID to delete", type=int)
    
    # Show project name before deletion
    current_project = db.get_project_by_id(project_id)
    if not current_project:
        click.echo(f"Project {project_id} not found.")
        return
    
    if click.confirm(f"Are you sure you want to delete project '{current_project[1]}'?"):
        if db.delete_project(project_id):
            click.echo(f"Project {project_id} deleted.")
        else:
            click.echo(f"Project {project_id} not found.")