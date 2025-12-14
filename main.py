import click
from config import Config


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config.load()


@cli.command()
@click.pass_context
def test(ctx):
    config = ctx.obj['config']
    click.echo(f"Config loaded successfully!")
    click.echo(f"Database path: {config.db_path}")


if __name__ == "__main__":
    cli()
