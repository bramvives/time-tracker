import click
from config import Config
from database import Database


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config.load()
    ctx.obj['db'] = Database(ctx.obj['config'].db_path)


@cli.command()
@click.pass_context
def test(ctx):
    config = ctx.obj['config']
    db = ctx.obj['db']
    click.echo(f"Config loaded successfully!")
    click.echo(f"Database path: {config.db_path}")
    click.echo(f"Database initialized at: {db.db_path}")


if __name__ == "__main__":
    cli()
