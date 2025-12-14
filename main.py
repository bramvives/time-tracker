import click
from config import Config
from database import Database
from commands.project import project


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config.load()
    ctx.obj['db'] = Database(ctx.obj['config'].db_path)


cli.add_command(project)  # type: ignore

if __name__ == "__main__":
    cli()
