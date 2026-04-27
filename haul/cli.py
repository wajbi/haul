"""Entry point for the haul CLI."""

import click
from haul import config as cfg


@click.group()
def cli():
    """haul — sync your dotfiles across machines."""
    pass


@cli.group()
def config():
    """Manage haul configuration."""
    pass


@config.command("show")
def config_show():
    """Print current configuration."""
    current = cfg.load_config()
    for key, value in current.items():
        click.echo(f"  {key}: {value}")


@config.command("get")
@click.argument("key")
def config_get(key: str):
    """Get a configuration value."""
    try:
        value = cfg.get(key)
        click.echo(f"{key} = {value}")
    except KeyError as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise click.Abort()


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """Set a configuration value."""
    # Coerce common types
    if value.lower() in ("true", "false"):
        value = value.lower() == "true"

    try:
        cfg.set_value(key, value)
        click.echo(click.style(f"Set {key} = {value}", fg="green"))
    except KeyError as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise click.Abort()


@config.command("init")
def config_init():
    """Create a default config file if none exists."""
    if cfg.CONFIG_PATH.exists():
        click.echo(f"Config already exists at {cfg.CONFIG_PATH}")
        return
    cfg.save_config(cfg.DEFAULT_CONFIG.copy())
    click.echo(click.style("Initialized default config.", fg="green"))


if __name__ == "__main__":
    cli()
