import click
from ..config import Config
from ..database import Database
from .commands.project import project
from .commands.time_entry import time


@click.group()
@click.pass_context
def cli(ctx):
    """Time Tracker CLI - Track time spent on projects"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config.load()
    ctx.obj['db'] = Database(ctx.obj['config'].db_path)


cli.add_command(project)
cli.add_command(time)


if __name__ == "__main__":
    cli()